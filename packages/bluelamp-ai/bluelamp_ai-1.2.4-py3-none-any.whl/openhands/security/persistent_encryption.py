"""
Persistent Encryption System
セッション間で暗号化キーを永続化するシステム
"""

import os
import json
import base64
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger('bluelamp.security.persistent_encryption')


class PersistentEncryption:
    """永続的な暗号化を提供するクラス"""
    
    def __init__(self):
        # デバイス固有のキーを生成
        self.key = self._get_or_create_device_key()
        self.cipher = Fernet(self.key)
        
    def _get_or_create_device_key(self) -> bytes:
        """デバイス固有の暗号化キーを取得または作成"""
        # デバイス固有の情報を使用してキーを導出
        device_id = self._get_device_id()
        
        # 固定のソルト（デバイスIDと組み合わせて使用）
        salt = b'bluelamp_cli_2024_secure_salt_v1'
        
        # PBKDF2でキーを導出
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(device_id.encode()))
        return key
        
    def _get_device_id(self) -> str:
        """デバイス固有のIDを生成"""
        # 複数の要素を組み合わせてデバイスIDを生成
        components = []
        
        # 1. ホームディレクトリパス
        components.append(str(Path.home()))
        
        # 2. ユーザー名
        try:
            import getpass
            components.append(getpass.getuser())
        except:
            components.append("unknown")
            
        # 3. マシン固有の情報
        try:
            import platform
            components.append(platform.node())
            components.append(platform.machine())
        except:
            pass
            
        # 4. 固定のシード（アプリケーション固有）
        components.append("bluelamp_cli_v1")
        
        # 全て結合してデバイスIDとする
        device_id = "|".join(components)
        return device_id
        
    def encrypt(self, text: str) -> str:
        """テキストを暗号化"""
        try:
            encrypted = self.cipher.encrypt(text.encode())
            return f"PERSISTENT:{base64.urlsafe_b64encode(encrypted).decode()}"
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return text
            
    def decrypt(self, encrypted_text: str) -> str:
        """暗号化されたテキストを復号化"""
        try:
            # 旧形式（ENCRYPTED:）の場合はそのまま返す（エラーになる）
            if encrypted_text.startswith("ENCRYPTED:"):
                logger.warning("Old encryption format detected, cannot decrypt")
                return ""
                
            if not encrypted_text.startswith("PERSISTENT:"):
                return encrypted_text
                
            encrypted_data = encrypted_text.replace("PERSISTENT:", "")
            decrypted = self.cipher.decrypt(base64.urlsafe_b64decode(encrypted_data))
            return decrypted.decode()
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return ""
            
    def is_encrypted(self, text: str) -> bool:
        """テキストが暗号化されているかチェック"""
        return text.startswith("PERSISTENT:") or text.startswith("ENCRYPTED:")


# シングルトンインスタンス
_persistent_encryption: Optional[PersistentEncryption] = None


def get_persistent_encryption() -> PersistentEncryption:
    """永続的暗号化のシングルトンインスタンスを取得"""
    global _persistent_encryption
    if _persistent_encryption is None:
        _persistent_encryption = PersistentEncryption()
    return _persistent_encryption