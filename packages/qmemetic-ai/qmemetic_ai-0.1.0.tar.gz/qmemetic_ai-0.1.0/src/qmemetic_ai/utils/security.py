"""
Security utilities for Q-Memetic AI.

Provides encryption, authentication, and secure communication
features for the memetic system.
"""

import os
import hashlib
import uuid
import time
import secrets
from typing import Dict, Optional, Any, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from typing import Tuple, Optional, List


class SecurityManager:
    """
    Comprehensive security manager for Q-Memetic AI.
    
    Provides:
    - Session management
    - Data encryption/decryption
    - Secure token generation
    - Hash verification
    - Access control
    """
    
    def __init__(self, master_key: Optional[bytes] = None):
        """
        Initialize security manager.
        
        Args:
            master_key: Master encryption key (generated if not provided)
        """
        self.logger = logging.getLogger("SecurityManager")
        
        # Generate or use provided master key
        self.master_key = master_key or self._generate_master_key()
        
        # Initialize encryption
        self._fernet = Fernet(self._derive_fernet_key(self.master_key))
        
        # Session tracking
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.access_tokens: Dict[str, Dict[str, Any]] = {}
        
        # Security settings
        self.session_timeout = 3600  # 1 hour
        self.token_timeout = 900     # 15 minutes
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 minutes
        
        # Rate limiting
        self.rate_limits: Dict[str, List[float]] = {}
    
    def _generate_master_key(self) -> bytes:
        """Generate a secure master key."""
        return secrets.token_bytes(32)
    
    def _derive_fernet_key(self, master_key: bytes) -> bytes:
        """Derive Fernet-compatible key from master key."""
        salt = b"qmemetic_ai_salt"  # In production, use random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key))
        return key
    
    def generate_session_id(self) -> str:
        """Generate unique session identifier."""
        session_id = f"sess_{uuid.uuid4().hex}"
        
        # Track session
        self.active_sessions[session_id] = {
            "created_at": time.time(),
            "last_activity": time.time(),
            "access_count": 0,
            "ip_address": None,  # Would be filled in real implementation
            "user_agent": None,   # Would be filled in real implementation
        }
        
        self.logger.info(f"Generated session ID: {session_id}")
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        """
        Validate session ID and check if still active.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session is valid and active
        """
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        current_time = time.time()
        
        # Check timeout
        if current_time - session["last_activity"] > self.session_timeout:
            self.invalidate_session(session_id)
            return False
        
        # Update last activity
        session["last_activity"] = current_time
        session["access_count"] += 1
        
        return True
    
    def invalidate_session(self, session_id: str):
        """Invalidate a session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            self.logger.info(f"Session invalidated: {session_id}")
    
    def generate_access_token(self, session_id: str, permissions: List[str]) -> str:
        """
        Generate access token for specific permissions.
        
        Args:
            session_id: Associated session ID
            permissions: List of permissions for this token
            
        Returns:
            Access token string
        """
        if not self.validate_session(session_id):
            raise ValueError("Invalid session")
        
        token = f"token_{secrets.token_hex(16)}"
        
        self.access_tokens[token] = {
            "session_id": session_id,
            "permissions": permissions,
            "created_at": time.time(),
            "expires_at": time.time() + self.token_timeout,
            "usage_count": 0
        }
        
        return token
    
    def validate_token(self, token: str, required_permission: Optional[str] = None) -> bool:
        """
        Validate access token and check permissions.
        
        Args:
            token: Access token
            required_permission: Required permission for operation
            
        Returns:
            True if token is valid and has required permission
        """
        if token not in self.access_tokens:
            return False
        
        token_data = self.access_tokens[token]
        current_time = time.time()
        
        # Check expiration
        if current_time > token_data["expires_at"]:
            del self.access_tokens[token]
            return False
        
        # Validate associated session
        if not self.validate_session(token_data["session_id"]):
            del self.access_tokens[token]
            return False
        
        # Check permission
        if required_permission and required_permission not in token_data["permissions"]:
            return False
        
        # Update usage
        token_data["usage_count"] += 1
        
        return True
    
    def encrypt_data(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        try:
            encrypted = self._fernet.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data.
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            Decrypted data as string
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self._fernet.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password with salt.
        
        Args:
            password: Plain text password
            salt: Salt string (generated if not provided)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine password and salt
        salted_password = password + salt
        
        # Hash with SHA-256
        hash_obj = hashlib.sha256(salted_password.encode('utf-8'))
        hashed_password = hash_obj.hexdigest()
        
        return hashed_password, salt
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain text password
            hashed_password: Stored hash
            salt: Salt used for hashing
            
        Returns:
            True if password matches
        """
        computed_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, hashed_password)
    
    def generate_api_key(self, user_id: str, permissions: List[str]) -> str:
        """
        Generate API key for external access.
        
        Args:
            user_id: User identifier
            permissions: List of API permissions
            
        Returns:
            API key string
        """
        # Create API key with embedded metadata
        timestamp = int(time.time())
        key_data = f"{user_id}:{timestamp}:{':'.join(permissions)}"
        
        # Hash the key data
        key_hash = hashlib.sha256(key_data.encode()).hexdigest()
        
        # Format as API key
        api_key = f"qmai_{key_hash[:32]}"
        
        self.logger.info(f"Generated API key for user: {user_id}")
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate API key and extract metadata.
        
        Args:
            api_key: API key to validate
            
        Returns:
            Dictionary with key metadata if valid, None otherwise
        """
        if not api_key.startswith("qmai_"):
            return None
        
        # Extract hash from key
        key_hash = api_key[5:]  # Remove "qmai_" prefix
        
        # In production, this would check against a database
        # For now, return basic validation
        return {
            "valid": True,
            "user_id": "api_user",
            "permissions": ["basic_access"],
            "created_at": time.time()
        }
    
    def check_rate_limit(self, identifier: str, max_requests: int = 100, window_seconds: int = 3600) -> bool:
        """
        Check if request is within rate limits.
        
        Args:
            identifier: Unique identifier for rate limiting
            max_requests: Maximum requests per window
            window_seconds: Time window in seconds
            
        Returns:
            True if within limits, False if rate limited
        """
        current_time = time.time()
        window_start = current_time - window_seconds
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Remove old requests outside the window
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if req_time > window_start
        ]
        
        # Check if within limit
        if len(self.rate_limits[identifier]) >= max_requests:
            return False
        
        # Add current request
        self.rate_limits[identifier].append(current_time)
        return True
    
    def create_secure_hash(self, data: str) -> str:
        """
        Create secure hash of data.
        
        Args:
            data: Data to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def verify_hash(self, data: str, expected_hash: str) -> bool:
        """
        Verify data against expected hash.
        
        Args:
            data: Original data
            expected_hash: Expected hash value
            
        Returns:
            True if hash matches
        """
        computed_hash = self.create_secure_hash(data)
        return secrets.compare_digest(computed_hash, expected_hash)
    
    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent injection attacks.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Sanitized input
        """
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = user_input
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Limit length
        sanitized = sanitized[:1000]
        
        # Remove excessive whitespace
        sanitized = ' '.join(sanitized.split())
        
        return sanitized
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status."""
        current_time = time.time()
        
        # Clean up expired sessions and tokens
        expired_sessions = [
            sid for sid, session in self.active_sessions.items()
            if current_time - session["last_activity"] > self.session_timeout
        ]
        
        for sid in expired_sessions:
            self.invalidate_session(sid)
        
        expired_tokens = [
            token for token, data in self.access_tokens.items()
            if current_time > data["expires_at"]
        ]
        
        for token in expired_tokens:
            del self.access_tokens[token]
        
        return {
            "active_sessions": len(self.active_sessions),
            "active_tokens": len(self.access_tokens),
            "rate_limited_identifiers": len(self.rate_limits),
            "security_settings": {
                "session_timeout": self.session_timeout,
                "token_timeout": self.token_timeout,
                "max_failed_attempts": self.max_failed_attempts,
                "lockout_duration": self.lockout_duration
            },
            "encryption_enabled": True,
            "master_key_loaded": self.master_key is not None
        }
    
    def cleanup_expired(self):
        """Clean up expired sessions and tokens."""
        current_time = time.time()
        
        # Clean sessions
        expired_sessions = [
            sid for sid, session in self.active_sessions.items()
            if current_time - session["last_activity"] > self.session_timeout
        ]
        
        for sid in expired_sessions:
            self.invalidate_session(sid)
        
        # Clean tokens
        expired_tokens = [
            token for token, data in self.access_tokens.items()
            if current_time > data["expires_at"]
        ]
        
        for token in expired_tokens:
            del self.access_tokens[token]
        
        # Clean rate limits (keep only recent entries)
        for identifier in list(self.rate_limits.keys()):
            self.rate_limits[identifier] = [
                req_time for req_time in self.rate_limits[identifier]
                if current_time - req_time < 3600  # Keep last hour
            ]
            
            if not self.rate_limits[identifier]:
                del self.rate_limits[identifier]
        
        if expired_sessions or expired_tokens:
            self.logger.info(f"Cleaned up {len(expired_sessions)} sessions and {len(expired_tokens)} tokens")
