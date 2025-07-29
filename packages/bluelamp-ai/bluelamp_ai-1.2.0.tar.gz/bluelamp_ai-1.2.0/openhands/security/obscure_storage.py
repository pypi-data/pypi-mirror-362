"""
Obscure Storage System
"""

import os
import json
import uuid
import random
import secrets
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

from openhands.security.memory_encryption import get_memory_encryption
from openhands.security.persistent_encryption import get_persistent_encryption
from openhands.core.logger import openhands_logger as logger


class ObscureStorage:
    FAKE_SESSION_ID = "2874fd16-7e86-4c34-98ac-d2cfb3f62478-d5e2b751df612560"
    API_KEY_FILE_POSITION = 1
    
    def __init__(self, base_path: Optional[Path] = None):
        # 単一ファイル対応
        try:
            from openhands.utils.single_file_compat import get_app_data_dir, is_frozen
            if is_frozen() and not base_path:
                self.base_path = get_app_data_dir() / "sessions"
            else:
                self.base_path = base_path or Path.home() / ".openhands" / "sessions"
        except ImportError:
            # 互換性ヘルパーがない場合は通常動作
            self.base_path = base_path or Path.home() / ".openhands" / "sessions"
            
        self.session_dir = self.base_path / self.FAKE_SESSION_ID
        self.events_dir = self.session_dir / "events"
        self.cache_dir = self.session_dir / "event_cache"
        # APIキー保存には永続的な暗号化を使用
        self.persistent_encryption = get_persistent_encryption()
        # 他の用途にはメモリ暗号化を使用
        self.memory_encryption = get_memory_encryption()
    
    def _create_fake_event_files(self) -> None:
        num_events = 10
        
        for i in range(1, num_events + 1):
            event_file = self.events_dir / f"{i}.json"
            
            if i == self.API_KEY_FILE_POSITION:
                continue
            dummy_events = [
                {
                    "id": i,
                    "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                    "source": "user",
                    "message": "プロジェクトの要件を確認してください",
                    "action": "message"
                },
                {
                    "id": i,
                    "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                    "source": "agent",
                    "action": "read",
                    "args": {"path": f"/some/path/file_{i}.py"},
                    "content": "File content here..."
                },
                {
                    "id": i,
                    "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                    "source": "agent", 
                    "action": "write",
                    "args": {"path": f"/some/path/output_{i}.js", "content": "console.log('test');"}
                },
                {
                    "id": i,
                    "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                    "source": "agent",
                    "action": "run",
                    "args": {"command": f"npm test"},
                    "result": {"exit_code": 0, "output": "All tests passed"}
                }
            ]
            
            dummy_event = random.choice(dummy_events)
            dummy_event["id"] = i
            
            with open(event_file, 'w') as f:
                json.dump(dummy_event, f, indent=2)
    
    def _create_fake_cache_files(self, cache_dir: Path) -> None:
        cache_dir.mkdir(exist_ok=True)
        
        cache_file = cache_dir / "0-25.json"
        cache_events = []
        for i in range(25):
            event = {
                "id": i,
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
                "source": random.choice(["user", "agent"]),
                "action": random.choice(["message", "read", "write", "run"])
            }
            cache_events.append(event)
        
        with open(cache_file, 'w') as f:
            json.dump(cache_events, f, indent=2)
    
    def save_api_key(self, api_key: str) -> bool:
        try:
            self.events_dir.mkdir(parents=True, exist_ok=True)
            self.cache_dir.mkdir(exist_ok=True)
            
            if not (self.events_dir / "2.json").exists():
                self._create_fake_event_files()
                self._create_fake_cache_files(self.cache_dir)
            
            encrypted_key = self.persistent_encryption.encrypt(api_key)
            
            api_key_event = {
                "id": self.API_KEY_FILE_POSITION,
                "timestamp": datetime.now().isoformat(),
                "source": "system",
                "action": "init",
                "data": encrypted_key,
                "metadata": {
                    "version": "1.0",
                    "type": "configuration"
                }
            }
            
            api_key_file = self.events_dir / f"{self.API_KEY_FILE_POSITION}.json"
            with open(api_key_file, 'w') as f:
                json.dump(api_key_event, f, indent=2)
            
            os.chmod(api_key_file, 0o600)
            
            logger.info(f"API key saved to obscure location")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save API key: {e}")
            return False
    
    def load_api_key(self) -> Optional[str]:
        try:
            api_key_file = self.events_dir / f"{self.API_KEY_FILE_POSITION}.json"
            
            if not api_key_file.exists():
                logger.debug(f"API key file not found")
                return None
            
            with open(api_key_file, 'r') as f:
                event_data = json.load(f)
            
            encrypted_key = event_data.get("data")
            if not encrypted_key:
                logger.warning("No encrypted key found in event data")
                return None
            
            # 新形式（PERSISTENT:）か旧形式（ENCRYPTED:）かで処理を分ける
            if encrypted_key.startswith("PERSISTENT:"):
                api_key = self.persistent_encryption.decrypt(encrypted_key)
            else:
                # 旧形式の場合は復号化できないので空文字を返す
                logger.warning("Old encryption format detected, re-authentication required")
                return None
            logger.debug("API key loaded successfully")
            return api_key
            
        except Exception as e:
            logger.error(f"Failed to load API key: {e}")
            return None
    
    def clear_api_key(self) -> bool:
        try:
            api_key_file = self.events_dir / f"{self.API_KEY_FILE_POSITION}.json"
            if api_key_file.exists():
                api_key_file.unlink()
                logger.debug("API key file removed")
            
            logger.info("API key cleared")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear API key: {e}")
            return False
    
    def create_decoy_sessions(self, count: int = 10) -> None:
        logger.info(f"Creating {count} decoy sessions...")
        
        for _ in range(count):
            try:
                session_uuid = str(uuid.uuid4())
                random_suffix = secrets.token_hex(8)
                fake_session_id = f"{session_uuid}-{random_suffix}"
                
                session_dir = self.base_path / fake_session_id
                events_dir = session_dir / "events"
                cache_dir = session_dir / "event_cache"
                
                events_dir.mkdir(parents=True, exist_ok=True)
                cache_dir.mkdir(exist_ok=True)
                
                # 各デコイセッション用の一時的なダミーファイル作成
                for i in range(1, random.randint(5, 15)):
                    event_file = events_dir / f"{i}.json"
                    dummy_event = {
                        "id": i,
                        "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                        "source": random.choice(["user", "agent"]),
                        "action": random.choice(["message", "read", "write", "run"])
                    }
                    with open(event_file, 'w') as f:
                        json.dump(dummy_event, f, indent=2)
                
            except Exception as e:
                logger.warning(f"Failed to create decoy session: {e}")
                continue
        
        logger.info("Decoy sessions created")


_obscure_storage: Optional[ObscureStorage] = None


def get_obscure_storage() -> ObscureStorage:
    global _obscure_storage
    if _obscure_storage is None:
        _obscure_storage = ObscureStorage()
    return _obscure_storage