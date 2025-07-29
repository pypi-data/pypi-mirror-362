"""
Memory Encryption Module

Provides encryption/decryption capabilities for sensitive data stored in memory,
specifically designed to protect system prompts from memory dump attacks.

This implements "temporal security" - data is encrypted 99.9% of the time,
and only decrypted for the brief moment when needed for AI communication.
"""

import base64
import threading
from typing import Optional

from openhands.core.logger import openhands_logger as logger

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    logger.warning("cryptography library not available. Memory encryption disabled.")
    ENCRYPTION_AVAILABLE = False


class MemoryEncryption:
    """
    Singleton class for encrypting/decrypting sensitive content in memory.
    
    Features:
    - Session-specific dynamic key generation
    - Thread-safe operations
    - Transparent encryption/decryption
    - Minimal performance impact
    """
    
    _instance: Optional['MemoryEncryption'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'MemoryEncryption':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the encryption system with a session-specific key."""
        if not ENCRYPTION_AVAILABLE:
            self.cipher = None
            logger.warning("Memory encryption disabled due to missing cryptography library")
            return
            
        # Generate a session-specific encryption key
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        logger.info("Memory encryption initialized with session-specific key")
    
    def encrypt(self, text: str) -> str:
        """
        Encrypt text content for secure memory storage.
        
        Args:
            text: Plain text to encrypt
            
        Returns:
            Encrypted text with ENCRYPTED: prefix, or original text if encryption unavailable
        """
        if not text or not ENCRYPTION_AVAILABLE or self.cipher is None:
            return text
            
        try:
            # Encrypt the text
            encrypted_bytes = self.cipher.encrypt(text.encode('utf-8'))
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('ascii')
            
            # Add prefix to identify encrypted content
            result = f"ENCRYPTED:{encrypted_b64}"
            
            # 詳細ログ（検証用）
            logger.info(f"🔒 MEMORY ENCRYPTION: {len(text)} chars -> {len(result)} chars")
            logger.info(f"🔒 Original preview: {text[:50]}...")
            logger.info(f"🔒 Encrypted preview: {result[:70]}...")
            
            logger.debug(
                f"Memory encryption: encrypted {len(text)} chars to {len(result)} chars",
                extra={'original_length': len(text), 'encrypted_length': len(result)}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Memory encryption failed: {e}")
            return text  # Fallback to plain text
    
    def decrypt(self, text: str) -> str:
        """
        Decrypt text content for AI communication.
        
        Args:
            text: Potentially encrypted text
            
        Returns:
            Decrypted plain text, or original text if not encrypted
        """
        if not text or not self.is_encrypted(text):
            return text
            
        if not ENCRYPTION_AVAILABLE or self.cipher is None:
            logger.warning("Cannot decrypt: encryption not available")
            return text
            
        try:
            # Remove the ENCRYPTED: prefix
            encrypted_b64 = text[10:]  # Remove "ENCRYPTED:" prefix
            
            # Decode and decrypt
            encrypted_bytes = base64.b64decode(encrypted_b64.encode('ascii'))
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            result = decrypted_bytes.decode('utf-8')
            
            # 詳細ログ（検証用）
            logger.info(f"🔓 MEMORY DECRYPTION: {len(text)} chars -> {len(result)} chars")
            logger.info(f"🔓 Encrypted preview: {text[:70]}...")
            logger.info(f"🔓 Decrypted preview: {result[:50]}...")
            
            logger.debug(
                f"Memory decryption: decrypted {len(text)} chars to {len(result)} chars",
                extra={'encrypted_length': len(text), 'decrypted_length': len(result)}
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Memory decryption failed: {e}")
            return text  # Fallback to original text
    
    def is_encrypted(self, text: str) -> bool:
        """
        Check if text is encrypted.
        
        Args:
            text: Text to check
            
        Returns:
            True if text is encrypted, False otherwise
        """
        return bool(text and text.startswith("ENCRYPTED:"))
    
    def get_encryption_status(self) -> dict:
        """
        Get current encryption system status.
        
        Returns:
            Dictionary with encryption system status information
        """
        return {
            'available': ENCRYPTION_AVAILABLE,
            'initialized': self.cipher is not None if ENCRYPTION_AVAILABLE else False,
            'key_length': len(self.key) if ENCRYPTION_AVAILABLE and hasattr(self, 'key') else 0,
        }


# Global instance for easy access
_memory_encryption = None

def get_memory_encryption() -> MemoryEncryption:
    """Get the global MemoryEncryption instance."""
    global _memory_encryption
    if _memory_encryption is None:
        _memory_encryption = MemoryEncryption()
    return _memory_encryption