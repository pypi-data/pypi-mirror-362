"""
Database models for Echo Sync Protocol.
"""
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .session import Base

class EchoNode(Base):
    """Model representing an EchoNode."""
    
    __tablename__ = "echo_nodes"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    version = Column(String, nullable=False)
    meta = Column('metadata', JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    states = relationship("NodeState", back_populates="node")
    conflicts = relationship("Conflict", back_populates="node")
    operations = relationship("SyncOperation", back_populates="node")

class NodeState(Base):
    """Model representing a node's state."""
    
    __tablename__ = "node_states"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("echo_nodes.id"), nullable=False)
    data = Column(JSON, nullable=False)
    version = Column(String, nullable=False)
    meta = Column('metadata', JSON, nullable=False, default=dict)
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    node = relationship("EchoNode", back_populates="states")

class Conflict(Base):
    """Model representing a synchronization conflict."""
    
    __tablename__ = "conflicts"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("echo_nodes.id"), nullable=False)
    resolution_strategy = Column(String, nullable=False)
    resolution_data = Column(JSON, nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    node = relationship("EchoNode", back_populates="conflicts")

class SyncOperation(Base):
    """Model representing a synchronization operation."""
    
    __tablename__ = "sync_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("echo_nodes.id"), nullable=False)
    operation_type = Column(String, nullable=False)  # push, pull, resolve
    status = Column(String, nullable=False)  # success, failed, pending
    error_message = Column(String, nullable=True)
    meta = Column('metadata', JSON, nullable=False, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    node = relationship("EchoNode", back_populates="operations")

class AuditLog(Base):
    """Model representing an audit log entry."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    details = Column(JSON, nullable=False, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow) 