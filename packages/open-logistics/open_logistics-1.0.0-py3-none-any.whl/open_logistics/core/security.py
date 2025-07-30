"""
Core security functionalities for the Open Logistics platform.

This module provides enterprise-grade security features including:
- AES-256 encryption/decryption
- JWT token management
- Role-based access control
- Security audit logging
- Classification level handling
"""

import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import jwt
from loguru import logger

from open_logistics.core.config import get_settings


class SecurityManager:
    """
    Manages security-related tasks like authentication, authorization,
    and data encryption.
    
    Provides enterprise-grade security features:
    - AES-256 encryption for sensitive data
    - JWT token generation and validation
    - Role-based access control
    - Security audit logging
    - Classification level management
    """

    def __init__(self):
        self.settings = get_settings()
        self._encryption_key = self._derive_encryption_key()
        self._fernet = Fernet(self._encryption_key)
        self._jwt_secret = self.settings.security.SECRET_KEY.encode()
        
        # Security audit log
        self._audit_log: List[Dict[str, Any]] = []
        
        # Role definitions
        self._roles = {
            "admin": {
                "permissions": ["read", "write", "delete", "configure", "audit"],
                "classification_levels": ["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"]
            },
            "operator": {
                "permissions": ["read", "write", "configure"],
                "classification_levels": ["UNCLASSIFIED", "CONFIDENTIAL"]
            },
            "analyst": {
                "permissions": ["read", "write"],
                "classification_levels": ["UNCLASSIFIED", "CONFIDENTIAL"]
            },
            "viewer": {
                "permissions": ["read"],
                "classification_levels": ["UNCLASSIFIED"]
            }
        }

    def _derive_encryption_key(self) -> bytes:
        """Derive encryption key from settings."""
        password = self.settings.security.SECRET_KEY.encode()
        salt = b"open_logistics_salt"  # In production, use random salt per installation
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypts the provided data using AES-256 encryption.
        
        Args:
            data: Raw data to encrypt
            
        Returns:
            Encrypted data
        """
        try:
            encrypted_data = self._fernet.encrypt(data)
            self._log_security_event("data_encrypted", {"data_size": len(data)})
            return encrypted_data
        except Exception as e:
            self._log_security_event("encryption_failed", {"error": str(e)})
            raise

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypts the provided data using AES-256 decryption.
        
        Args:
            encrypted_data: Encrypted data to decrypt
            
        Returns:
            Decrypted data
        """
        try:
            decrypted_data = self._fernet.decrypt(encrypted_data)
            self._log_security_event("data_decrypted", {"data_size": len(decrypted_data)})
            return decrypted_data
        except Exception as e:
            self._log_security_event("decryption_failed", {"error": str(e)})
            raise

    def encrypt_string(self, text: str) -> str:
        """
        Encrypts a string and returns base64 encoded result.
        
        Args:
            text: String to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        encrypted_bytes = self.encrypt_data(text.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')

    def decrypt_string(self, encrypted_text: str) -> str:
        """
        Decrypts a base64 encoded encrypted string.
        
        Args:
            encrypted_text: Base64 encoded encrypted string
            
        Returns:
            Decrypted string
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
        decrypted_bytes = self.decrypt_data(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')

    def generate_jwt_token(self, user_id: str, role: str, expires_in_hours: int = 24) -> str:
        """
        Generate a JWT token for user authentication.
        
        Args:
            user_id: User identifier
            role: User role
            expires_in_hours: Token expiration time in hours
            
        Returns:
            JWT token string
        """
        try:
            payload = {
                "user_id": user_id,
                "role": role,
                "classification_level": self.settings.security.CLASSIFICATION_LEVEL,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
                "iss": "open_logistics",
                "permissions": self._roles.get(role, {}).get("permissions", [])
            }
            
            token = jwt.encode(payload, self._jwt_secret, algorithm="HS256")
            
            self._log_security_event("jwt_token_generated", {
                "user_id": user_id,
                "role": role,
                "expires_in_hours": expires_in_hours
            })
            
            return token
            
        except Exception as e:
            self._log_security_event("jwt_generation_failed", {"error": str(e)})
            raise

    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate and decode a JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=["HS256"])
            
            self._log_security_event("jwt_token_validated", {
                "user_id": payload.get("user_id"),
                "role": payload.get("role")
            })
            
            return payload
            
        except jwt.ExpiredSignatureError:
            self._log_security_event("jwt_token_expired", {"token": token[:20] + "..."})
            return None
        except jwt.InvalidTokenError:
            self._log_security_event("jwt_token_invalid", {"token": token[:20] + "..."})
            return None
        except Exception as e:
            self._log_security_event("jwt_validation_failed", {"error": str(e)})
            return None

    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """
        Check if a user role has the required permission.
        
        Args:
            user_role: User's role
            required_permission: Permission to check
            
        Returns:
            True if permission is granted
        """
        role_permissions = self._roles.get(user_role, {}).get("permissions", [])
        has_permission = required_permission in role_permissions
        
        self._log_security_event("permission_check", {
            "user_role": user_role,
            "required_permission": required_permission,
            "granted": has_permission
        })
        
        return has_permission

    def check_classification_access(self, user_role: str, data_classification: str) -> bool:
        """
        Check if a user role can access data with given classification level.
        
        Args:
            user_role: User's role
            data_classification: Data classification level
            
        Returns:
            True if access is granted
        """
        role_levels = self._roles.get(user_role, {}).get("classification_levels", [])
        has_access = data_classification in role_levels
        
        self._log_security_event("classification_access_check", {
            "user_role": user_role,
            "data_classification": data_classification,
            "granted": has_access
        })
        
        return has_access

    def hash_password(self, password: str) -> str:
        """
        Hash a password using PBKDF2 with SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        salt = secrets.token_bytes(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        # Combine salt and hash
        combined = salt + pwdhash
        hashed_password = base64.urlsafe_b64encode(combined).decode('utf-8')
        
        self._log_security_event("password_hashed", {"password_length": len(password)})
        
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password is correct
        """
        try:
            combined = base64.urlsafe_b64decode(hashed_password.encode('utf-8'))
            salt = combined[:32]
            stored_hash = combined[32:]
            
            pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            
            is_valid = hmac.compare_digest(stored_hash, pwdhash)
            
            self._log_security_event("password_verified", {
                "password_length": len(password),
                "valid": is_valid
            })
            
            return is_valid
            
        except Exception as e:
            self._log_security_event("password_verification_failed", {"error": str(e)})
            return False

    def generate_api_key(self, user_id: str, description: str = "") -> str:
        """
        Generate a secure API key for a user.
        
        Args:
            user_id: User identifier
            description: Optional description for the key
            
        Returns:
            Generated API key
        """
        # Generate random key
        key_bytes = secrets.token_bytes(32)
        api_key = base64.urlsafe_b64encode(key_bytes).decode('utf-8')
        
        # Add prefix for identification
        prefixed_key = f"ol_{api_key}"
        
        self._log_security_event("api_key_generated", {
            "user_id": user_id,
            "description": description,
            "key_prefix": prefixed_key[:10] + "..."
        })
        
        return prefixed_key

    def get_security_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get security audit log entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of audit log entries
        """
        return self._audit_log[-limit:]

    def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """
        Log a security event for audit purposes.
        
        Args:
            event_type: Type of security event
            details: Event details
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "classification_level": self.settings.security.CLASSIFICATION_LEVEL
        }
        
        self._audit_log.append(log_entry)
        
        # Log to file as well
        logger.info(f"Security event: {event_type}", extra={"security_event": log_entry})
        
        # Keep only last 1000 entries in memory
        if len(self._audit_log) > 1000:
            self._audit_log = self._audit_log[-1000:] 