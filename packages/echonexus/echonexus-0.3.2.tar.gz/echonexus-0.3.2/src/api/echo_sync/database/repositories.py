"""
Database repositories for Echo Sync Protocol.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .models import EchoNode, NodeState, Conflict, SyncOperation, AuditLog

class EchoNodeRepository:
    """Repository for EchoNode operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_node(self, node_id: str) -> Optional[EchoNode]:
        """Get a node by ID."""
        return self.db.query(EchoNode).filter(EchoNode.id == node_id).first()

    def create_node(
        self,
        node_id: str,
        name: str | None = None,
        version: str = "1.0",
        is_active: bool = True,
        metadata: Dict[str, Any] | None = None,
    ) -> EchoNode:
        """Create a new node."""
        node = EchoNode(
            id=node_id,
            name=name,
            version=version,
            meta=metadata or {},
            is_active=is_active,
        )
        self.db.add(node)
        self.db.commit()
        return node

    def update_node(self, node_id: str, **kwargs) -> Optional[EchoNode]:
        """Update a node's attributes."""
        node = self.get_node(node_id)
        if node:
            for key, value in kwargs.items():
                setattr(node, key, value)
            self.db.commit()
        return node

class NodeStateRepository:
    """Repository for NodeState operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_current_state(self, node_id: str) -> Optional[NodeState]:
        """Get the current state of a node."""
        return self.db.query(NodeState).filter(
            NodeState.node_id == node_id,
            NodeState.is_current == True
        ).first()

    def get_state_history(self, node_id: str, limit: int = 100) -> List[NodeState]:
        """Get the state history of a node."""
        return self.db.query(NodeState).filter(
            NodeState.node_id == node_id
        ).order_by(desc(NodeState.timestamp)).limit(limit).all()

    def create_state(self, node_id: str, data: Dict[str, Any], version: str, metadata: Dict[str, Any] = None) -> NodeState:
        """Create a new state for a node."""
        # Mark current state as not current
        current_state = self.get_current_state(node_id)
        if current_state:
            current_state.is_current = False

        # Create new state
        state = NodeState(
            node_id=node_id,
            data=data,
            version=version,
            meta=metadata or {},
            is_current=True
        )
        self.db.add(state)
        self.db.commit()
        return state

class ConflictRepository:
    """Repository for Conflict operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_unresolved_conflicts(self, node_id: str) -> List[Conflict]:
        """Get unresolved conflicts for a node."""
        return self.db.query(Conflict).filter(
            Conflict.node_id == node_id,
            Conflict.is_resolved == False
        ).all()

    def create_conflict(self, node_id: str, resolution_strategy: str, resolution_data: Dict[str, Any]) -> Conflict:
        """Create a new conflict."""
        conflict = Conflict(
            node_id=node_id,
            resolution_strategy=resolution_strategy,
            resolution_data=resolution_data
        )
        self.db.add(conflict)
        self.db.commit()
        return conflict

    def resolve_conflict(self, conflict_id: int) -> Optional[Conflict]:
        """Mark a conflict as resolved."""
        conflict = self.db.query(Conflict).filter(Conflict.id == conflict_id).first()
        if conflict:
            conflict.is_resolved = True
            conflict.resolved_at = datetime.utcnow()
            self.db.commit()
        return conflict

class SyncOperationRepository:
    """Repository for SyncOperation operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def create_operation(self, node_id: str, operation_type: str, status: str, error_message: str = None, metadata: Dict[str, Any] = None) -> SyncOperation:
        """Create a new sync operation."""
        operation = SyncOperation(
            node_id=node_id,
            operation_type=operation_type,
            status=status,
            error_message=error_message,
            meta=metadata or {}
        )
        self.db.add(operation)
        self.db.commit()
        return operation

    def get_recent_operations(self, node_id: str, limit: int = 100) -> List[SyncOperation]:
        """Get recent sync operations for a node."""
        return self.db.query(SyncOperation).filter(
            SyncOperation.node_id == node_id
        ).order_by(desc(SyncOperation.timestamp)).limit(limit).all()

class AuditLogRepository:
    """Repository for AuditLog operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, user_id: str, action: str, resource_type: str, resource_id: str, details: Dict[str, Any] = None) -> AuditLog:
        """Create a new audit log entry."""
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
        self.db.add(log)
        self.db.commit()
        return log

    def get_recent_logs(self, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs."""
        return self.db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit).all() 