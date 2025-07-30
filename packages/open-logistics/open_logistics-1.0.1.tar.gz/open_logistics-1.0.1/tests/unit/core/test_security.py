"""
Unit tests for core security module.
"""
from open_logistics.core.security import SecurityManager

class TestSecurityManager:
    """Tests for the SecurityManager."""

    def test_encryption_decryption(self):
        """Test that data can be encrypted and decrypted."""
        manager = SecurityManager()
        original_data = b"secret data"
        encrypted = manager.encrypt_data(original_data)
        decrypted = manager.decrypt_data(encrypted)
        assert encrypted != original_data
        assert decrypted == original_data 