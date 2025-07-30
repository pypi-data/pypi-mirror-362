"""
Memory Guard: Hallucination Prevention System for EchoNexus

This module implements fail-safe mechanisms to prevent information fabrication
and enforce memory boundary compliance across all EchoNexus modules.
"""

import os
import sys
import logging
import functools
from typing import Any, Optional, Dict, List, Callable
from contextlib import contextmanager

# Add tushell to path for memory operations
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../tushell'))
from tushell.mod.rst import TushellResonance

class MemoryBoundaryError(Exception):
    """Raised when memory boundary is violated."""
    pass

class HallucinationGuard:
    """
    Prevents information fabrication by enforcing memory boundaries.
    
    All memory operations must go through this guard to ensure:
    1. No fabricated responses
    2. Proper error handling for missing memory
    3. Centralized memory access through tushell
    4. Audit trail for all memory operations
    """
    
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.memory = TushellResonance()
        self.access_log = []
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for memory access audit trail."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - MemoryGuard - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def _log_access(self, operation: str, key: str, success: bool, error: str = None):
        """Log all memory access attempts."""
        log_entry = {
            'operation': operation,
            'key': key,
            'success': success,
            'error': error,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        self.access_log.append(log_entry)
        
        if success:
            self.logger.info(f"Memory {operation} successful: {key}")
        else:
            self.logger.error(f"Memory {operation} failed: {key} - {error}")
    
    def get_memory(self, key: str, allow_none: bool = False) -> Optional[str]:
        """
        Safely retrieve memory content.
        
        Args:
            key: Memory key to retrieve
            allow_none: Whether to allow None returns (default: False)
            
        Returns:
            Memory content or None if allowed
            
        Raises:
            MemoryBoundaryError: If memory not found and allow_none=False
        """
        try:
            # Validate key exists first
            if not self.memory.validate_memory_boundary(key):
                error = f"Memory key '{key}' does not exist"
                self._log_access('get', key, False, error)
                if allow_none:
                    return None
                raise MemoryBoundaryError(error)
            
            content = self.memory.get_memory(key)
            self._log_access('get', key, True)
            return content
            
        except Exception as e:
            self._log_access('get', key, False, str(e))
            if allow_none:
                return None
            raise MemoryBoundaryError(f"Failed to retrieve memory '{key}': {e}")
    
    def post_memory(self, key: str, content: str) -> bool:
        """
        Safely store memory content.
        
        Args:
            key: Memory key to store
            content: Content to store
            
        Returns:
            True if successful
            
        Raises:
            MemoryBoundaryError: If storage fails
        """
        try:
            success = self.memory.post_memory(key, content)
            self._log_access('post', key, success)
            return success
            
        except Exception as e:
            self._log_access('post', key, False, str(e))
            raise MemoryBoundaryError(f"Failed to store memory '{key}': {e}")
    
    def scan_keys(self, pattern: str = "*") -> List[str]:
        """
        Safely scan for memory keys.
        
        Args:
            pattern: Pattern to match keys
            
        Returns:
            List of matching keys
            
        Raises:
            MemoryBoundaryError: If scan fails
        """
        try:
            keys = self.memory.scan_keys(pattern)
            self._log_access('scan', pattern, True)
            return keys
            
        except Exception as e:
            self._log_access('scan', pattern, False, str(e))
            raise MemoryBoundaryError(f"Failed to scan keys with pattern '{pattern}': {e}")
    
    def require_memory(self, key: str) -> str:
        """
        Require memory to exist, fail if not found.
        
        Args:
            key: Memory key that must exist
            
        Returns:
            Memory content
            
        Raises:
            MemoryBoundaryError: If memory not found
        """
        return self.get_memory(key, allow_none=False)
    
    def safe_memory(self, key: str, default: str = "[Memory not available]") -> str:
        """
        Safe memory retrieval with explicit default.
        
        Args:
            key: Memory key to retrieve
            default: Default value if memory not found
            
        Returns:
            Memory content or default
        """
        try:
            content = self.get_memory(key, allow_none=True)
            return content if content is not None else default
        except Exception:
            return default
    
    def get_access_log(self) -> List[Dict]:
        """Get the memory access audit log."""
        return self.access_log.copy()
    
    def clear_access_log(self):
        """Clear the memory access audit log."""
        self.access_log.clear()

# Global memory guard instance
_memory_guard = None

def get_memory_guard() -> HallucinationGuard:
    """Get the global memory guard instance."""
    global _memory_guard
    if _memory_guard is None:
        _memory_guard = HallucinationGuard()
    return _memory_guard

def memory_boundary_check(func: Callable) -> Callable:
    """
    Decorator to enforce memory boundary compliance.
    
    Use this decorator on functions that access memory to ensure
    they go through the hallucination guard.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        guard = get_memory_guard()
        
        # Inject memory guard into function if it accepts it
        if 'memory_guard' in func.__code__.co_varnames:
            kwargs['memory_guard'] = guard
        
        try:
            return func(*args, **kwargs)
        except MemoryBoundaryError:
            # Re-raise memory boundary errors
            raise
        except Exception as e:
            # Log unexpected errors
            guard.logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise
    
    return wrapper

@contextmanager
def memory_context(strict: bool = True):
    """
    Context manager for memory operations.
    
    Args:
        strict: Whether to enforce strict memory boundaries
        
    Yields:
        HallucinationGuard instance
    """
    guard = HallucinationGuard(strict_mode=strict)
    try:
        yield guard
    finally:
        # Log final statistics
        total_ops = len(guard.access_log)
        successful_ops = sum(1 for log in guard.access_log if log['success'])
        guard.logger.info(f"Memory context closed: {successful_ops}/{total_ops} operations successful")

# Convenience functions for common operations
def get_memory(key: str, allow_none: bool = False) -> Optional[str]:
    """Convenience function for getting memory."""
    return get_memory_guard().get_memory(key, allow_none)

def post_memory(key: str, content: str) -> bool:
    """Convenience function for posting memory."""
    return get_memory_guard().post_memory(key, content)

def scan_keys(pattern: str = "*") -> List[str]:
    """Convenience function for scanning keys."""
    return get_memory_guard().scan_keys(pattern)

def require_memory(key: str) -> str:
    """Convenience function for requiring memory."""
    return get_memory_guard().require_memory(key)

def safe_memory(key: str, default: str = "[Memory not available]") -> str:
    """Convenience function for safe memory retrieval."""
    return get_memory_guard().safe_memory(key, default)

# Error classes for specific memory boundary violations
class FabricationError(MemoryBoundaryError):
    """Raised when code attempts to fabricate information."""
    pass

class DirectRedisAccessError(MemoryBoundaryError):
    """Raised when code bypasses tushell for direct Redis access."""
    pass

class PlaceholderFunctionError(MemoryBoundaryError):
    """Raised when placeholder functions are called in production."""
    pass

def prevent_fabrication(func: Callable) -> Callable:
    """
    Decorator to prevent information fabrication.
    
    Use this on functions that might be tempted to fabricate responses.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # Check for common fabrication patterns
        if isinstance(result, str):
            fabrication_patterns = [
                "placeholder",
                "mock",
                "fake",
                "generated",
                "artificial",
                "synthetic"
            ]
            
            result_lower = result.lower()
            for pattern in fabrication_patterns:
                if pattern in result_lower:
                    raise FabricationError(f"Function {func.__name__} appears to fabricate information: contains '{pattern}'")
        
        return result
    
    return wrapper

def audit_memory_compliance(module_path: str) -> Dict[str, Any]:
    """
    Audit a module for memory boundary compliance.
    
    Args:
        module_path: Path to module to audit
        
    Returns:
        Dict with audit results
    """
    audit_results = {
        'module': module_path,
        'violations': [],
        'recommendations': [],
        'compliant': True
    }
    
    try:
        with open(module_path, 'r') as f:
            content = f.read()
        
        # Check for direct Redis access
        if 'redis.Redis' in content or 'redis.from_url' in content:
            audit_results['violations'].append({
                'type': 'direct_redis_access',
                'message': 'Module accesses Redis directly instead of using tushell'
            })
            audit_results['compliant'] = False
        
        # Check for eval() usage
        if 'eval(' in content:
            audit_results['violations'].append({
                'type': 'eval_usage',
                'message': 'Module uses unsafe eval() function'
            })
            audit_results['compliant'] = False
        
        # Check for placeholder functions
        if 'placeholder' in content.lower() or 'mock' in content.lower():
            audit_results['violations'].append({
                'type': 'placeholder_function',
                'message': 'Module contains placeholder functions'
            })
            audit_results['compliant'] = False
        
        # Check for proper memory guard usage
        if 'memory_guard' not in content and any(pattern in content for pattern in ['get_memory', 'post_memory', 'scan_keys']):
            audit_results['recommendations'].append({
                'type': 'memory_guard_usage',
                'message': 'Consider using memory_guard decorator for memory operations'
            })
    
    except Exception as e:
        audit_results['error'] = str(e)
        audit_results['compliant'] = False
    
    return audit_results