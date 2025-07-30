"""
Echo Sync Protocol Data Models

This module defines the data models used by the Echo Sync Protocol API.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class NodeState(BaseModel):
    """Represents the state of an EchoNode."""
    node_id: str = Field(..., description="Unique identifier of the node")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this state was recorded")
    data: Dict[str, Any] = Field(default_factory=dict, description="The node's state data")
    version: str = Field(..., description="Version identifier for this state")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the state")

class SyncOptions(BaseModel):
    """Options for synchronizing node states."""
    force: bool = Field(default=False, description="Force synchronization even if there are conflicts")
    timeout: int = Field(default=30, description="Timeout in seconds for sync operations")
    priority: int = Field(default=0, description="Priority level for this sync operation")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters to apply during sync")

class ConflictResolution(BaseModel):
    """Strategy and data for resolving conflicts."""
    strategy: str = Field(..., description="The conflict resolution strategy to use")
    resolution_data: Dict[str, Any] = Field(default_factory=dict, description="Data needed for the resolution strategy")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this resolution was created")

class SyncResponse(BaseModel):
    """Response from a sync operation."""
    success: bool = Field(..., description="Whether the sync was successful")
    message: str = Field(..., description="Description of the sync result")
    conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Any conflicts that were found")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the sync completed")

class NodeStatus(BaseModel):
    """Current status of an EchoNode."""
    node_id: str = Field(..., description="Unique identifier of the node")
    is_online: bool = Field(..., description="Whether the node is currently online")
    last_sync: Optional[datetime] = Field(None, description="When the node last synced")
    version: str = Field(..., description="Current version of the node")
    status: str = Field(..., description="Current status of the node")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional status metadata")

class ResolutionResult(BaseModel):
    """Result of a conflict resolution operation."""
    success: bool = Field(..., description="Whether the resolution was successful")
    message: str = Field(..., description="Description of the resolution result")
    resolved_state: Optional[NodeState] = Field(None, description="The resolved state if successful")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the resolution completed")

class ReplayData(BaseModel):
    """Data model for replaying the sync ritual."""
    node_id: str = Field(..., description="Unique identifier of the node")
    current_state: Optional[NodeState] = Field(None, description="The current state of the node")
    recent_operations: List[Dict[str, Any]] = Field(default_factory=list, description="Recent operations performed on the node")
    unresolved_conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Unresolved conflicts for the node")
