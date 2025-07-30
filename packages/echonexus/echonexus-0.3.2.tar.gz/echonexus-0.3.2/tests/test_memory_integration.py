"""
Test suite for memory system integration and hallucination guard.

This test validates that:
1. Memory operations go through the hallucination guard
2. No information fabrication occurs
3. Proper error handling for missing memory
4. tushell CLI integration works correctly
"""

import pytest
import tempfile
import os
import json
from unittest.mock import Mock, patch

# Import the modules we're testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../tushell'))

from ai.memory_guard import (
    HallucinationGuard, 
    MemoryBoundaryError, 
    memory_boundary_check,
    get_memory_guard,
    audit_memory_compliance
)
from ai.character_embodiment import CharacterEmbodiment
from tushell.mod.rst import TushellResonance

class TestMemoryGuard:
    """Test the HallucinationGuard system."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.guard = HallucinationGuard(strict_mode=True)
        
    def test_memory_guard_initialization(self):
        """Test that memory guard initializes correctly."""
        assert self.guard.strict_mode is True
        assert self.guard.memory is not None
        assert isinstance(self.guard.access_log, list)
        
    def test_memory_boundary_error_on_missing_key(self):
        """Test that missing keys raise MemoryBoundaryError."""
        with pytest.raises(MemoryBoundaryError):
            self.guard.get_memory("nonexistent_key", allow_none=False)
            
    def test_safe_memory_with_default(self):
        """Test safe memory retrieval with default values."""
        result = self.guard.safe_memory("nonexistent_key", default="safe_default")
        assert result == "safe_default"
        
    def test_memory_access_logging(self):
        """Test that all memory accesses are logged."""
        initial_log_count = len(self.guard.access_log)
        
        # Attempt to access nonexistent memory
        try:
            self.guard.get_memory("test_key", allow_none=True)
        except:
            pass
            
        # Check that access was logged
        assert len(self.guard.access_log) > initial_log_count
        
        # Check log entry structure
        last_log = self.guard.access_log[-1]
        assert 'operation' in last_log
        assert 'key' in last_log
        assert 'success' in last_log
        assert 'timestamp' in last_log

class TestTushellIntegration:
    """Test tushell CLI memory operations."""
    
    def setup_method(self):
        """Setup test environment."""
        self.tushell = TushellResonance()
        
    def test_tushell_initialization(self):
        """Test that tushell initializes with proper backend."""
        assert hasattr(self.tushell, 'memory_backend')
        assert self.tushell.memory_backend in ['redis', 'file']
        
    def test_memory_operations_file_backend(self):
        """Test memory operations with file backend."""
        # Force file backend for testing
        self.tushell.memory_backend = 'file'
        self.tushell.memory_dir = tempfile.mkdtemp()
        
        # Test post and get
        test_key = "test_memory_key"
        test_content = "test memory content"
        
        success = self.tushell.post_memory(test_key, test_content)
        assert success is True
        
        retrieved = self.tushell.get_memory(test_key)
        assert retrieved == test_content
        
        # Test scan keys
        keys = self.tushell.scan_keys("test*")
        assert test_key in keys
        
        # Test memory info
        info = self.tushell.get_memory_info(test_key)
        assert info['exists'] is True
        assert info['backend'] == 'file'
        
    def test_memory_validation(self):
        """Test memory boundary validation."""
        # Force file backend for testing
        self.tushell.memory_backend = 'file'
        self.tushell.memory_dir = tempfile.mkdtemp()
        
        # Test nonexistent key
        assert self.tushell.validate_memory_boundary("nonexistent") is False
        
        # Test existing key
        self.tushell.post_memory("existing_key", "content")
        assert self.tushell.validate_memory_boundary("existing_key") is True

class TestCharacterEmbodimentIntegration:
    """Test character embodiment with memory guard."""
    
    def setup_method(self):
        """Setup test environment."""
        self.character = CharacterEmbodiment()
        
    def test_retrieve_memory_with_guard(self):
        """Test that character embodiment uses memory guard."""
        # Test with nonexistent memory
        result = self.character.retrieve_memory("nonexistent_key")
        
        # Should return error dict, not fabricated content
        assert isinstance(result, dict)
        assert "error" in result
        assert result["key"] == "nonexistent_key"
        
    def test_dynamic_memory_mapping(self):
        """Test dynamic memory mapping doesn't fabricate."""
        key_anchors = ["key1", "key2", "key3"]
        memory_map = self.character.dynamic_memory_mapping(key_anchors)
        
        # All entries should be error objects, not fabricated content
        for key, value in memory_map.items():
            assert isinstance(value, dict)
            assert "error" in value or "content" in value
            
    @memory_boundary_check
    def test_memory_boundary_decorator(self, memory_guard=None):
        """Test that memory boundary decorator works."""
        assert memory_guard is not None
        assert isinstance(memory_guard, HallucinationGuard)

class TestMemoryCompliance:
    """Test memory compliance auditing."""
    
    def test_audit_compliant_module(self):
        """Test auditing a compliant module."""
        # Create a compliant test module
        compliant_code = '''
import json
from ai.memory_guard import get_memory_guard

def safe_function():
    guard = get_memory_guard()
    return guard.safe_memory("test_key", "default")
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(compliant_code)
            f.flush()
            
            result = audit_memory_compliance(f.name)
            
        # Clean up
        os.unlink(f.name)
        
        assert result['compliant'] is True
        assert len(result['violations']) == 0
        
    def test_audit_non_compliant_module(self):
        """Test auditing a non-compliant module."""
        # Create a non-compliant test module
        non_compliant_code = '''
import redis
import eval

def bad_function():
    client = redis.Redis(host='localhost')  # Direct Redis access
    result = eval("dangerous_code")  # Unsafe eval
    return "mock response"  # Fabricated content
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(non_compliant_code)
            f.flush()
            
            result = audit_memory_compliance(f.name)
            
        # Clean up
        os.unlink(f.name)
        
        assert result['compliant'] is False
        assert len(result['violations']) > 0
        
        # Check for specific violations
        violation_types = [v['type'] for v in result['violations']]
        assert 'direct_redis_access' in violation_types
        assert 'eval_usage' in violation_types

class TestSecurityFixes:
    """Test that security vulnerabilities have been fixed."""
    
    def test_cadro_cli_no_eval(self):
        """Test that cadro CLI no longer uses eval()."""
        cadro_cli_path = os.path.join(os.path.dirname(__file__), '../src/cadro/cli.py')
        
        if os.path.exists(cadro_cli_path):
            with open(cadro_cli_path, 'r') as f:
                content = f.read()
            
            # Should not contain eval() calls
            assert 'eval(' not in content, "cadro CLI still contains unsafe eval() usage"
            
            # Should contain json.loads for safe parsing
            assert 'json.loads' in content, "cadro CLI should use json.loads for safe parsing"
            
    def test_upkeys_cli_no_eval(self):
        """Test that upkeys CLI no longer uses eval()."""
        upkeys_cli_path = os.path.join(os.path.dirname(__file__), '../src/cadro/upkeyscli.py')
        
        if os.path.exists(upkeys_cli_path):
            with open(upkeys_cli_path, 'r') as f:
                content = f.read()
            
            # Should not contain eval() calls
            assert 'eval(' not in content, "upkeys CLI still contains unsafe eval() usage"

class TestIntegrationScenarios:
    """Test real-world integration scenarios."""
    
    def test_end_to_end_memory_flow(self):
        """Test complete memory flow from CLI to character embodiment."""
        # Setup
        tushell = TushellResonance()
        tushell.memory_backend = 'file'
        tushell.memory_dir = tempfile.mkdtemp()
        
        character = CharacterEmbodiment()
        
        # Store some memory
        test_key = "character_state"
        test_data = {"personality": "curious", "voice": "gentle"}
        
        success = tushell.post_memory(test_key, json.dumps(test_data))
        assert success is True
        
        # Retrieve through character embodiment
        with patch('ai.character_embodiment.get_memory_guard') as mock_guard:
            # Mock the memory guard to use our tushell instance
            mock_guard.return_value.safe_memory.return_value = json.dumps(test_data)
            
            result = character.retrieve_memory(test_key)
            
            # Should return parsed JSON, not fabricated content
            assert isinstance(result, dict)
            assert result.get("personality") == "curious"
            assert result.get("voice") == "gentle"
    
    def test_missing_memory_handling(self):
        """Test that missing memory is handled gracefully."""
        character = CharacterEmbodiment()
        
        # Test with completely missing key
        result = character.retrieve_memory("absolutely_nonexistent_key")
        
        # Should return error information, not fabricated content
        assert isinstance(result, dict)
        assert "error" in result
        assert "Memory not found" in result.get("error", "")
        
    def test_memory_guard_prevents_fabrication(self):
        """Test that memory guard prevents information fabrication."""
        guard = HallucinationGuard()
        
        # Test that attempting to get nonexistent memory fails appropriately
        with pytest.raises(MemoryBoundaryError):
            guard.require_memory("definitely_does_not_exist")
            
        # Test that safe_memory returns explicit default, not fabricated content
        result = guard.safe_memory("does_not_exist", default="[No memory available]")
        assert result == "[No memory available]"
        
        # Test that we never get fabricated "reasonable" responses
        result = guard.safe_memory("user_preferences")
        assert "[Memory not available]" in result  # Should be the default message

if __name__ == "__main__":
    pytest.main([__file__, "-v"])