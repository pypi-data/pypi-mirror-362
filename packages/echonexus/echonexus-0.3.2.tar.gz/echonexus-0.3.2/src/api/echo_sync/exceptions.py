"""
Echo Sync Protocol Exceptions

This module defines custom exceptions used by the Echo Sync Protocol API.
"""

class EchoSyncError(Exception):
    """Base exception for all Echo Sync Protocol errors."""
    pass

class NodeNotFoundError(EchoSyncError):
    """Raised when a requested node cannot be found."""
    pass

class SyncError(EchoSyncError):
    """Raised when a synchronization operation fails."""
    pass

class ConflictError(EchoSyncError):
    """Raised when there are unresolvable conflicts during sync."""
    pass

class ValidationError(EchoSyncError):
    """Raised when node state validation fails."""
    pass

class AuthenticationError(EchoSyncError):
    """Raised when authentication fails."""
    pass

class AuthorizationError(EchoSyncError):
    """Raised when the user is not authorized to perform an operation."""
    pass

class TimeoutError(EchoSyncError):
    """Raised when a sync operation times out."""
    pass

class VersionMismatchError(EchoSyncError):
    """Raised when there is a version mismatch during sync."""
    pass

class NetworkError(EchoSyncError):
    """Raised when there are network-related issues during sync."""
    pass

class StorageError(EchoSyncError):
    """Raised when there are issues with state storage."""
    pass 