"""
Tests for EchoSyncService implementation.
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..services.sync_service import EchoSyncService
from ..models import NodeState, SyncOptions, ConflictResolution
from ..exceptions import SyncError
from ..database.repositories import (
    EchoNodeRepository,
    NodeStateRepository,
    ConflictRepository,
    SyncOperationRepository,
    AuditLogRepository
)

# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    from ..database.models import Base
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sync_service(db_session, test_node):
    """Create a fresh EchoSyncService instance for each test."""
    service = EchoSyncService(db_session)
    service._nodes[test_node.id] = test_node
    return service

@pytest.fixture
def test_node(db_session):
    """Create a test node."""
    node_repo = EchoNodeRepository(db_session)
    return node_repo.create_node(
        node_id="test_node",
        name="Test Node",
        is_active=True
    )

@pytest.fixture
def test_state():
    """Create a test state."""
    return NodeState(
        node_id="test_node",
        data={"key": "value"},
        version="1.0",
        metadata={"source": "test"}
    )

import asyncio


def test_push_state_success(sync_service, test_node, test_state):
    """Test successful state push."""
    options = SyncOptions(force=False)
    response = asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    assert response.success
    assert response.message == "State pushed successfully"
    assert response.timestamp is not None

def test_push_state_conflict(sync_service, test_node, test_state):
    """Test state push with conflict."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Push conflicting state
    conflicting_state = NodeState(
        node_id="test_node",
        data={"key": "different_value"},
        version="1.0",
        metadata={"source": "test"}
    )
    
    response = asyncio.run(sync_service.push_state("test_node", conflicting_state, options))
    
    assert not response.success
    assert response.message == "Conflicts detected"
    assert len(response.conflicts) > 0

def test_pull_state_success(sync_service, test_node, test_state):
    """Test successful state pull."""
    # Push state first
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Pull state
    pulled_state = asyncio.run(sync_service.pull_state("test_node", options))
    
    assert pulled_state.node_id == test_state.node_id
    assert pulled_state.data == test_state.data
    assert pulled_state.version == test_state.version

def test_pull_state_not_found(sync_service, test_node):
    """Test pulling non-existent state."""
    options = SyncOptions(force=False)
    
    with pytest.raises(SyncError) as exc_info:
        asyncio.run(sync_service.pull_state("test_node", options))

    assert "No state found" in str(exc_info.value)

def test_get_node_status(sync_service, test_node, test_state):
    """Test getting node status."""
    # Push state first
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Get status
    status = asyncio.run(sync_service.get_node_status("test_node"))
    
    assert status.node_id == "test_node"
    assert status.is_online
    assert status.version == test_state.version
    assert status.status == "online"

def test_resolve_conflicts_prefer_local(sync_service, test_node, test_state):
    """Test conflict resolution with prefer_local strategy."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Create conflict
    conflicting_state = NodeState(
        node_id="test_node",
        data={"key": "different_value"},
        version="1.0",
        metadata={"source": "test"}
    )
    asyncio.run(sync_service.push_state("test_node", conflicting_state, options))
    
    # Resolve conflicts
    resolution = ConflictResolution(strategy="prefer_local")
    result = asyncio.run(sync_service.resolve_conflicts("test_node", resolution))
    
    assert result.success
    assert "Resolved" in result.message
    assert result.resolved_state is not None

def test_resolve_conflicts_prefer_remote(sync_service, test_node, test_state):
    """Test conflict resolution with prefer_remote strategy."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Create conflict
    conflicting_state = NodeState(
        node_id="test_node",
        data={"key": "different_value"},
        version="1.0",
        metadata={"source": "test"}
    )
    asyncio.run(sync_service.push_state("test_node", conflicting_state, options))
    
    # Resolve conflicts
    resolution = ConflictResolution(strategy="prefer_remote")
    result = asyncio.run(sync_service.resolve_conflicts("test_node", resolution))
    
    assert result.success
    assert "Resolved" in result.message
    assert result.resolved_state is not None

@pytest.mark.xfail(reason="merge strategy not fully implemented")
def test_resolve_conflicts_merge(sync_service, test_node, test_state):
    """Test conflict resolution with merge strategy."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Create conflict
    conflicting_state = NodeState(
        node_id="test_node",
        data={"key": "different_value", "new_key": "new_value"},
        version="1.0",
        metadata={"source": "test", "new_meta": "value"}
    )
    asyncio.run(sync_service.push_state("test_node", conflicting_state, options))
    
    # Resolve conflicts
    resolution = ConflictResolution(strategy="merge")
    result = asyncio.run(sync_service.resolve_conflicts("test_node", resolution))
    
    assert result.success
    assert "Resolved" in result.message
    assert result.resolved_state is not None
    assert "new_key" in result.resolved_state.data
    assert "new_meta" in result.resolved_state.metadata

def test_merge_states(sync_service):
    """Test state merging functionality."""
    local = {
        "key1": "value1",
        "nested": {
            "key2": "value2",
            "key3": "value3"
        },
        "list": [1, 2, 3]
    }
    
    remote = {
        "key1": "new_value1",
        "nested": {
            "key2": "new_value2",
            "key4": "value4"
        },
        "list": [3, 4, 5],
        "new_key": "new_value"
    }
    
    merged = sync_service._merge_states(local, remote)
    
    assert merged["key1"] == "new_value1"
    assert merged["nested"]["key2"] == "new_value2"
    assert merged["nested"]["key3"] == "value3"
    assert merged["nested"]["key4"] == "value4"
    assert set(merged["list"]) == {1, 2, 3, 4, 5}
    assert merged["new_key"] == "new_value"

def test_detect_conflicts_ml(sync_service, test_node, test_state):
    """Test conflict detection using machine learning-based conflict detection."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Create new state with potential conflicts
    new_state = NodeState(
        node_id="test_node",
        data={"key": "different_value", "new_key": "new_value"},
        version="2.0",
        metadata={"source": "test", "new_meta": "value"}
    )
    
    # Detect conflicts using ML
    conflicts = asyncio.run(sync_service.detect_conflicts_ml("test_node", new_state))
    
    assert len(conflicts) > 0
    assert any(conflict["type"] == "version_mismatch" for conflict in conflicts)
    assert any(conflict["type"] == "data_conflict" for conflict in conflicts)

def test_replay_sync_ritual(sync_service, test_node, test_state):
    """Test replaying the sync ritual for a specific node."""
    # Push initial state
    options = SyncOptions(force=False)
    asyncio.run(sync_service.push_state("test_node", test_state, options))
    
    # Replay sync ritual
    replay_data = asyncio.run(sync_service.replay_sync_ritual("test_node"))
    
    assert replay_data["node_id"] == "test_node"
    assert replay_data["current_state"].node_id == "test_node"
    assert replay_data["current_state"].data == test_state.data
    assert replay_data["current_state"].version == test_state.version
    assert len(replay_data["recent_operations"]) > 0
    assert len(replay_data["unresolved_conflicts"]) == 0
