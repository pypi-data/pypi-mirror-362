"""
Echo Sync Protocol API Routes

This module defines the API endpoints for the Echo Sync Protocol.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from .models import (
    NodeState,
    SyncOptions,
    ConflictResolution,
    SyncResponse,
    NodeStatus,
    ResolutionResult
)
from .services.sync_service import EchoSyncService
from .middleware.auth import get_current_user
from .exceptions import NodeNotFoundError, SyncError

router = APIRouter()

@router.post("/nodes/{node_id}/push")
async def push_state(
    node_id: str,
    state: NodeState,
    options: Optional[SyncOptions] = None,
    current_user = Depends(get_current_user)
) -> SyncResponse:
    """
    Push state to a specific node.
    
    Args:
        node_id: The ID of the target node
        state: The state to push
        options: Optional sync options
        current_user: The authenticated user
    
    Returns:
        SyncResponse: The result of the push operation
    """
    try:
        service = EchoSyncService()
        return await service.push_state(node_id, state, options or SyncOptions())
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SyncError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/nodes/{node_id}/pull")
async def pull_state(
    node_id: str,
    options: Optional[SyncOptions] = None,
    current_user = Depends(get_current_user)
) -> NodeState:
    """
    Pull state from a specific node.
    
    Args:
        node_id: The ID of the source node
        options: Optional sync options
        current_user: The authenticated user
    
    Returns:
        NodeState: The pulled state
    """
    try:
        service = EchoSyncService()
        return await service.pull_state(node_id, options or SyncOptions())
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SyncError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{node_id}/status")
async def get_node_status(
    node_id: str,
    current_user = Depends(get_current_user)
) -> NodeStatus:
    """
    Get real-time status of a node.
    
    Args:
        node_id: The ID of the node
        current_user: The authenticated user
    
    Returns:
        NodeStatus: The current status of the node
    """
    try:
        service = EchoSyncService()
        return await service.get_node_status(node_id)
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/nodes/{node_id}/conflicts/resolve")
async def resolve_conflicts(
    node_id: str,
    resolution: ConflictResolution,
    current_user = Depends(get_current_user)
) -> ResolutionResult:
    """
    Resolve conflicts between nodes.
    
    Args:
        node_id: The ID of the node
        resolution: The conflict resolution strategy and data
        current_user: The authenticated user
    
    Returns:
        ResolutionResult: The result of the conflict resolution
    """
    try:
        service = EchoSyncService()
        return await service.resolve_conflicts(node_id, resolution)
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SyncError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{node_id}/history")
async def get_node_history(
    node_id: str,
    limit: int = 100,
    current_user = Depends(get_current_user)
) -> List[NodeState]:
    """
    Get node state history.
    
    Args:
        node_id: The ID of the node
        limit: Maximum number of history entries to return
        current_user: The authenticated user
    
    Returns:
        List[NodeState]: The node's state history
    """
    try:
        service = EchoSyncService()
        return await service.get_node_history(node_id, limit)
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{node_id}/replay")
async def replay_sync_ritual(
    node_id: str,
    current_user = Depends(get_current_user)
) -> dict:
    """
    Replay the sync ritual for a specific node.
    
    Args:
        node_id: The ID of the node
        current_user: The authenticated user
    
    Returns:
        dict: The replay data for the sync ritual
    """
    try:
        service = EchoSyncService()
        return await service.replay_sync_ritual(node_id)
    except NodeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
