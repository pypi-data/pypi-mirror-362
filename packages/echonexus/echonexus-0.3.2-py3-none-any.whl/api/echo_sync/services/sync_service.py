"""
Echo Sync Protocol Service

This module implements the core synchronization functionality for the Echo Sync Protocol.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from ..database.repositories import (
    EchoNodeRepository,
    NodeStateRepository,
    ConflictRepository,
    SyncOperationRepository,
    AuditLogRepository
)
from ..models import (
    NodeState,
    SyncOptions,
    ConflictResolution,
    SyncResponse,
    NodeStatus,
    ResolutionResult
)
from ..exceptions import (
    NodeNotFoundError,
    SyncError,
    ConflictError,
    ValidationError,
    TimeoutError,
    VersionMismatchError
)
from ..config import settings
from ..monitoring import monitor

class EchoSyncService:
    """Service for managing EchoNode synchronization."""
    
    def __init__(self, db: Session):
        """Initialize the sync service with database session."""
        self.db = db
        self.node_repo = EchoNodeRepository(db)
        self.state_repo = NodeStateRepository(db)
        self.conflict_repo = ConflictRepository(db)
        self.operation_repo = SyncOperationRepository(db)
        self.audit_repo = AuditLogRepository(db)
        self._nodes: Dict[str, NodeState] = {}  # Placeholder for node storage
    
    async def push_state(self, node_id: str, state: NodeState, options: SyncOptions) -> SyncResponse:
        """
        Push state to a specific node.
        
        Args:
            node_id: The ID of the target node
            state: The state to push
            options: Sync options
        
        Returns:
            SyncResponse: The result of the push operation
        
        Raises:
            NodeNotFoundError: If the target node doesn't exist
            SyncError: If the push operation fails
            ConflictError: If there are conflicts and force=False
        """
        start_time = datetime.utcnow()
        try:
            # Create sync operation record
            operation = self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="push",
                status="pending"
            )

            # Validate the state
            self._validate_state(state)
            
            # Check if node exists
            if node_id not in self._nodes:
                raise NodeNotFoundError(f"Node {node_id} not found")
            
            # Get current state
            current_state = self.state_repo.get_current_state(node_id)
            
            # Check for conflicts if not forcing
            if current_state and not options.force:
                conflicts = self._detect_conflicts(current_state, state)
                if conflicts:
                    # Record conflicts
                    for conflict in conflicts:
                        self.conflict_repo.create_conflict(
                            node_id=node_id,
                            resolution_strategy="pending",
                            resolution_data=conflict
                        )
                    
                    # Update operation status
                    self.operation_repo.create_operation(
                        node_id=node_id,
                        operation_type="push",
                        status="conflict",
                        error_message="Conflicts detected"
                    )
                    
                    # Track conflict
                    monitor.track_conflict(
                        resolution_strategy=settings.sync.default_resolution_strategy
                    )
                    
                    # Track operation
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    monitor.track_operation(
                        operation_type="push",
                        status="conflict",
                        duration=duration
                    )
                    
                    return SyncResponse(
                        success=False,
                        message="Conflicts detected",
                        conflicts=conflicts
                    )

            # Update state
            new_state = self.state_repo.create_state(
                node_id=node_id,
                data=state.data,
                version=state.version,
                metadata=state.metadata
            )

            # Update operation status
            self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="push",
                status="success"
            )

            # Log audit
            self.audit_repo.create_log(
                user_id="system",
                action="push_state",
                resource_type="node",
                resource_id=node_id,
                details={"version": state.version}
            )

            # Update metrics
            monitor.update_node_state_size(
                node_id=node_id,
                size_bytes=len(str(state.data))
            )
            monitor.update_node_status(
                node_id=node_id,
                status="active"
            )

            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="push",
                status="success",
                duration=duration
            )

            return SyncResponse(
                success=True,
                message="State pushed successfully",
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            # Log error
            self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="push",
                status="error",
                error_message=str(e)
            )

            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="push",
                status="error",
                duration=duration
            )

            raise SyncError(f"Failed to push state: {str(e)}")
    
    async def pull_state(self, node_id: str, options: SyncOptions) -> NodeState:
        """
        Pull state from a specific node.
        
        Args:
            node_id: The ID of the source node
            options: Sync options
        
        Returns:
            NodeState: The pulled state
        
        Raises:
            NodeNotFoundError: If the source node doesn't exist
            SyncError: If the pull operation fails
        """
        start_time = datetime.utcnow()
        try:
            # Create sync operation record
            operation = self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="pull",
                status="pending"
            )

            # Get current state
            state = self.state_repo.get_current_state(node_id)
            if not state:
                raise ValueError(f"No state found for node {node_id}")

            # Update operation status
            self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="pull",
                status="success"
            )

            # Log audit
            self.audit_repo.create_log(
                user_id="system",
                action="pull_state",
                resource_type="node",
                resource_id=node_id,
                details={"version": state.version}
            )

            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="pull",
                status="success",
                duration=duration
            )

            return state
            
        except Exception as e:
            # Log error
            self.operation_repo.create_operation(
                node_id=node_id,
                operation_type="pull",
                status="error",
                error_message=str(e)
            )

            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="pull",
                status="error",
                duration=duration
            )

            raise SyncError(f"Failed to pull state: {str(e)}")
    
    async def get_node_status(self, node_id: str) -> NodeStatus:
        """
        Get real-time status of a node.
        
        Args:
            node_id: The ID of the node
        
        Returns:
            NodeStatus: The current status of the node
        
        Raises:
            NodeNotFoundError: If the node doesn't exist
        """
        try:
            # Get node
            node = self.node_repo.get_node(node_id)
            if not node:
                raise ValueError(f"Node {node_id} not found")

            # Get current state
            current_state = self.state_repo.get_current_state(node_id)
            
            # Get recent operations
            recent_ops = self.operation_repo.get_recent_operations(node_id, limit=5)
            
            # Get unresolved conflicts
            conflicts = self.conflict_repo.get_unresolved_conflicts(node_id)

            # Determine status
            status = "online" if node.is_active else "offline"
            if conflicts:
                status = "conflict"
            elif recent_ops and recent_ops[0].status == "error":
                status = "error"

            # Update metrics
            monitor.update_node_status(node_id=node_id, status=status)
            if current_state:
                monitor.update_node_state_size(
                    node_id=node_id,
                    size_bytes=len(str(current_state.data))
                )

            return NodeStatus(
                node_id=node_id,
                is_online=node.is_active,
                last_sync=current_state.created_at if current_state else None,
                version=current_state.version if current_state else "unknown",
                status=status,
                metadata={
                    "conflict_count": len(conflicts),
                    "recent_operations": [op.operation_type for op in recent_ops]
                }
            )

        except Exception as e:
            raise ValueError(f"Failed to get node status: {str(e)}")
    
    async def resolve_conflicts(
        self,
        node_id: str,
        resolution: ConflictResolution
    ) -> ResolutionResult:
        """
        Resolve conflicts between nodes.
        
        Args:
            node_id: The ID of the node
            resolution: The conflict resolution strategy and data
        
        Returns:
            ResolutionResult: The result of the conflict resolution
        
        Raises:
            NodeNotFoundError: If the node doesn't exist
            ConflictError: If the resolution fails
        """
        start_time = datetime.utcnow()
        try:
            # Get unresolved conflicts
            conflicts = self.conflict_repo.get_unresolved_conflicts(node_id)
            if not conflicts:
                return ResolutionResult(
                    success=True,
                    message="No conflicts to resolve"
                )

            # Apply resolution strategy
            resolved_state = None
            for conflict in conflicts:
                if resolution.strategy == "prefer_local":
                    # Keep local state
                    local = self.state_repo.get_current_state(node_id)
                    if local:
                        resolved_state = NodeState(
                            node_id=node_id,
                            data=local.data,
                            version=local.version,
                            metadata=local.meta,
                        )
                elif resolution.strategy == "prefer_remote":
                    # Use remote state
                    resolved_state = NodeState(
                        node_id=node_id,
                        data=conflict.resolution_data.get("remote_state", {}),
                        version=conflict.resolution_data.get("remote_version", "unknown"),
                        metadata=conflict.resolution_data.get("remote_metadata", {})
                    )
                elif resolution.strategy == "merge":
                    # Merge states
                    local_state = self.state_repo.get_current_state(node_id)
                    remote_state = conflict.resolution_data.get("remote_state", {})
                    merged_data = self._merge_states(
                        local_state.data if local_state else {},
                        remote_state
                    )
                    resolved_state = NodeState(
                        node_id=node_id,
                        data=merged_data,
                        version=f"{local_state.version}+{conflict.resolution_data.get('remote_version', 'unknown')}",
                        metadata=self._merge_metadata(
                            local_state.meta if local_state else {},
                            conflict.resolution_data.get("remote_metadata", {})
                        )
                    )

                # Mark conflict as resolved
                self.conflict_repo.resolve_conflict(conflict.id)

            if resolved_state:
                # Create new state
                self.state_repo.create_state(
                    node_id=node_id,
                    data=resolved_state.data,
                    version=resolved_state.version,
                    metadata=resolved_state.metadata
                )

                # Log resolution
                self.audit_repo.create_log(
                    user_id="system",
                    action="resolve_conflicts",
                    resource_type="node",
                    resource_id=node_id,
                    details={
                        "strategy": resolution.strategy,
                        "resolved_count": len(conflicts)
                    }
                )

                # Update metrics
                monitor.update_node_state_size(
                    node_id=node_id,
                    size_bytes=len(str(resolved_state.data))
                )
                monitor.update_node_status(node_id=node_id, status="active")

                # Track operation
                duration = (datetime.utcnow() - start_time).total_seconds()
                monitor.track_operation(
                    operation_type="resolve_conflicts",
                    status="success",
                    duration=duration
                )
                monitor.track_conflict(
                    resolution_strategy=resolution.strategy,
                    resolved=True
                )

                return ResolutionResult(
                    success=True,
                    message=f"Resolved {len(conflicts)} conflicts using {resolution.strategy}",
                    resolved_state=resolved_state
                )

            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="resolve_conflicts",
                status="error",
                duration=duration
            )

            return ResolutionResult(
                success=False,
                message="Failed to resolve conflicts"
            )

        except Exception as e:
            # Track operation
            duration = (datetime.utcnow() - start_time).total_seconds()
            monitor.track_operation(
                operation_type="resolve_conflicts",
                status="error",
                duration=duration
            )
            raise ConflictError(f"Failed to resolve conflicts: {str(e)}")
    
    async def get_node_history(self, node_id: str, limit: int) -> List[NodeState]:
        """
        Get node state history.
        
        Args:
            node_id: The ID of the node
            limit: Maximum number of history entries to return
        
        Returns:
            List[NodeState]: The node's state history
        
        Raises:
            NodeNotFoundError: If the node doesn't exist
        """
        if node_id not in self._nodes:
            raise NodeNotFoundError(f"Node {node_id} not found")
        
        # TODO: Implement actual history tracking
        return [self._nodes[node_id]]  # Placeholder
    
    def _validate_state(self, state: NodeState) -> None:
        """
        Validate a node state.
        
        Args:
            state: The state to validate
        
        Raises:
            ValidationError: If the state is invalid
        """
        if not state.node_id:
            raise ValidationError("Node ID is required")
        if not state.version:
            raise ValidationError("Version is required")
    
    def _detect_conflicts(
        self,
        current_state: NodeState,
        new_state: NodeState
    ) -> List[Dict[str, Any]]:
        """
        Detect conflicts between states.
        
        Args:
            current_state: The current state
            new_state: The new state
        
        Returns:
            List[Dict[str, Any]]: List of detected conflicts
        """
        conflicts = []
        
        # Check version conflicts
        if current_state.version != new_state.version:
            conflicts.append({
                "type": "version_mismatch",
                "current_version": current_state.version,
                "new_version": new_state.version
            })

        # Check data conflicts
        for key in set(current_state.data.keys()) & set(new_state.data.keys()):
            if current_state.data[key] != new_state.data[key]:
                conflicts.append({
                    "type": "data_conflict",
                    "key": key,
                    "current_value": current_state.data[key],
                    "new_value": new_state.data[key]
                })

        return conflicts

    def _merge_states(self, local: Dict[str, Any], remote: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two states using a deep merge strategy."""
        result = local.copy()
        
        for key, value in remote.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_states(result[key], value)
                elif isinstance(value, list) and isinstance(result[key], list):
                    result[key] = list(set(result[key] + value))
                else:
                    # Prefer remote value in case of conflict
                    result[key] = value
            else:
                result[key] = value
                
        return result

    def _merge_metadata(self, local: Dict[str, Any], remote: Dict[str, Any]) -> Dict[str, Any]:
        """Merge metadata dictionaries."""
        return self._merge_states(local, remote) 

    async def replay_sync_ritual(self, node_id: str) -> dict:
        """
        Replay the sync ritual for a specific node.
        
        Args:
            node_id: The ID of the node
        
        Returns:
            dict: The replay data for the sync ritual
        
        Raises:
            NodeNotFoundError: If the node doesn't exist
        """
        try:
            # Get node
            node = self.node_repo.get_node(node_id)
            if not node:
                raise ValueError(f"Node {node_id} not found")

            # Get current state
            current_state = self.state_repo.get_current_state(node_id)
            
            # Get recent operations
            recent_ops = self.operation_repo.get_recent_operations(node_id, limit=5)
            
            # Get unresolved conflicts
            conflicts = self.conflict_repo.get_unresolved_conflicts(node_id)

            # Prepare replay data
            replay_data = {
                "node_id": node_id,
                "current_state": current_state,
                "recent_operations": recent_ops,
                "unresolved_conflicts": conflicts
            }

            return replay_data

        except Exception as e:
            raise ValueError(f"Failed to replay sync ritual: {str(e)}")

    async def detect_conflicts_ml(self, node_id: str, new_state: NodeState) -> List[Dict[str, Any]]:
        """
        Detect conflicts using machine learning-based conflict detection.
        
        Args:
            node_id: The ID of the node
            new_state: The new state
        
        Returns:
            List[Dict[str, Any]]: List of detected conflicts
        
        Raises:
            NodeNotFoundError: If the node doesn't exist
        """
        try:
            # Get current state
            current_state = self.state_repo.get_current_state(node_id)
            if not current_state:
                raise ValueError(f"No state found for node {node_id}")

            # Use machine learning model to detect conflicts
            conflicts = self._ml_model_detect_conflicts(current_state, new_state)

            return conflicts

        except Exception as e:
            raise ValueError(f"Failed to detect conflicts using ML: {str(e)}")

    def _ml_model_detect_conflicts(self, current_state: NodeState, new_state: NodeState) -> List[Dict[str, Any]]:
        """
        Basic conflict detection between states.
        
        Note: ML-based conflict detection was removed to reduce dependencies.
        Install echonexus[ml] and implement advanced ML conflict detection if needed.
        
        Args:
            current_state: The current state
            new_state: The new state
        
        Returns:
            List[Dict[str, Any]]: List of detected conflicts
        """
        conflicts = []

        # Basic conflict detection logic
        if current_state.version != new_state.version:
            conflicts.append({
                "type": "version_mismatch",
                "current_version": current_state.version,
                "new_version": new_state.version
            })

        for key in set(current_state.data.keys()) & set(new_state.data.keys()):
            if current_state.data[key] != new_state.data[key]:
                conflicts.append({
                    "type": "data_conflict",
                    "key": key,
                    "current_value": current_state.data[key],
                    "new_value": new_state.data[key]
                })

        return conflicts
