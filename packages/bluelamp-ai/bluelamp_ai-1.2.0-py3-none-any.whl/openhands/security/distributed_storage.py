"""
Distributed Storage System
APIキーを複数のファイルに分散して保存するシステム
"""

import os
import json
import random
import secrets
from pathlib import Path
from typing import Any, Optional, List, Dict, Tuple
from datetime import datetime, timedelta
import logging

from openhands.security.persistent_encryption import get_persistent_encryption
from openhands.security.memory_encryption import get_memory_encryption
from openhands.core.logger import openhands_logger as logger


class DistributedStorage:
    """APIキーを分散保存するストレージシステム"""
    
    def __init__(self, base_path: Optional[Path] = None):
        # 単一ファイル対応
        try:
            from openhands.utils.single_file_compat import get_app_data_dir, is_frozen
            if is_frozen() and not base_path:
                self.base_path = get_app_data_dir() / "sessions"
            else:
                self.base_path = base_path or Path.home() / ".openhands" / "sessions"
        except ImportError:
            self.base_path = base_path or Path.home() / ".openhands" / "sessions"
        
        # インデックスファイルの場所（複数箇所に冗長保存）
        self.index_locations = [
            Path.home() / ".openhands" / ".index",
            Path.home() / ".config" / "bluelamp" / ".idx",
            Path.home() / ".local" / "share" / "bluelamp" / ".index"
        ]
        
        # 暗号化システム
        self.persistent_encryption = get_persistent_encryption()
        self.memory_encryption = get_memory_encryption()
        
        # 分割数（セキュリティと性能のバランス）
        self.split_count = 3
        
    def save_api_key(self, api_key: str) -> bool:
        """APIキーを分散保存"""
        try:
            logger.info("Starting distributed storage of API key")
            
            # 1. APIキーを分割
            parts = self._split_key(api_key)
            
            # 2. 各パートをランダムな場所に保存
            locations = []
            for i, part in enumerate(parts):
                location = self._generate_random_location(i)
                if self._save_part(location, part):
                    locations.append(location)
                else:
                    # 一部でも失敗したらロールバック
                    self._rollback_saves(locations)
                    return False
            
            # 3. デコイファイルも生成
            self._create_decoy_files(num_decoys=20)
            
            # 4. インデックス情報を保存（復元に必要）
            index_data = {
                "version": "1.0",
                "locations": locations,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
                "checksum": self._calculate_checksum(api_key)
            }
            
            # 5. インデックスを複数箇所に保存（冗長性）
            if not self._save_index(index_data):
                self._rollback_saves(locations)
                return False
            
            logger.info("API key distributed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save distributed key: {e}")
            return False
    
    def load_api_key(self) -> Optional[str]:
        """分散保存されたAPIキーを復元"""
        try:
            logger.debug("Loading distributed API key")
            
            # 1. インデックスファイルを読み込み
            index_data = self._load_index()
            if not index_data:
                logger.debug("No index file found")
                return None
            
            # 2. 有効期限チェック
            expires_at = datetime.fromisoformat(index_data['expires_at'])
            if datetime.now() > expires_at:
                logger.info("API key expired")
                self.clear_api_key()
                return None
            
            # 3. 各パートを収集
            parts = []
            for location in sorted(index_data['locations'], key=lambda x: x['order']):
                part = self._load_part(location)
                if not part:
                    logger.error(f"Failed to load part from {location}")
                    return None
                parts.append(part)
            
            # 4. APIキーを復元
            api_key = ''.join(parts)
            
            # 5. チェックサム検証
            if self._calculate_checksum(api_key) != index_data.get('checksum'):
                logger.error("Checksum verification failed")
                return None
            
            logger.debug("API key loaded successfully")
            return api_key
            
        except Exception as e:
            logger.error(f"Failed to load distributed key: {e}")
            return None
    
    def clear_api_key(self) -> bool:
        """分散保存されたAPIキーをクリア"""
        try:
            # インデックスを読み込み
            index_data = self._load_index()
            if index_data:
                # 各パートを削除
                for location in index_data.get('locations', []):
                    self._delete_part(location)
            
            # インデックスファイルを削除
            for index_path in self.index_locations:
                if index_path.exists():
                    index_path.unlink()
            
            logger.info("Distributed API key cleared")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear distributed key: {e}")
            return False
    
    def _split_key(self, api_key: str) -> List[str]:
        """APIキーを複数のパートに分割"""
        key_len = len(api_key)
        part_size = key_len // self.split_count
        
        parts = []
        for i in range(self.split_count):
            if i == self.split_count - 1:
                # 最後のパートは残り全部
                parts.append(api_key[i * part_size:])
            else:
                parts.append(api_key[i * part_size:(i + 1) * part_size])
        
        return parts
    
    def _generate_random_location(self, order: int) -> Dict[str, Any]:
        """ランダムな保存場所を生成"""
        session_id = f"session-{secrets.token_hex(8)}"
        file_num = random.randint(1, 50)
        
        return {
            "session": session_id,
            "file": f"events/{file_num}.json",
            "order": order
        }
    
    def _save_part(self, location: Dict[str, Any], part: str) -> bool:
        """APIキーのパートを保存"""
        try:
            # ディレクトリ作成
            session_dir = self.base_path / location['session']
            events_dir = session_dir / "events"
            events_dir.mkdir(parents=True, exist_ok=True)
            
            # データを暗号化
            encrypted_part = self.persistent_encryption.encrypt(part)
            
            # イベントファイルとして保存（本物のイベントに見せかける）
            event_data = {
                "id": int(location['file'].split('/')[1].split('.')[0]),
                "timestamp": datetime.now().isoformat(),
                "source": "system",
                "action": random.choice(["init", "update", "sync"]),
                "data": encrypted_part,
                "metadata": {
                    "version": "1.0",
                    "type": random.choice(["configuration", "state", "cache"])
                }
            }
            
            # ファイルに書き込み
            file_path = session_dir / location['file']
            with open(file_path, 'w') as f:
                json.dump(event_data, f, indent=2)
            
            # パーミッション設定
            os.chmod(file_path, 0o600)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save part: {e}")
            return False
    
    def _load_part(self, location: Dict[str, Any]) -> Optional[str]:
        """APIキーのパートを読み込み"""
        try:
            file_path = self.base_path / location['session'] / location['file']
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r') as f:
                event_data = json.load(f)
            
            encrypted_part = event_data.get('data')
            if not encrypted_part:
                return None
            
            # 復号化
            part = self.persistent_encryption.decrypt(encrypted_part)
            return part
            
        except Exception as e:
            logger.error(f"Failed to load part: {e}")
            return None
    
    def _delete_part(self, location: Dict[str, Any]) -> None:
        """パートを削除"""
        try:
            file_path = self.base_path / location['session'] / location['file']
            if file_path.exists():
                file_path.unlink()
                
            # セッションディレクトリが空なら削除
            session_dir = self.base_path / location['session']
            if session_dir.exists() and not any(session_dir.rglob('*')):
                session_dir.rmdir()
                
        except Exception as e:
            logger.warning(f"Failed to delete part: {e}")
    
    def _save_index(self, index_data: Dict) -> bool:
        """インデックス情報を複数箇所に保存"""
        encrypted_index = self.persistent_encryption.encrypt(json.dumps(index_data))
        
        saved_count = 0
        for index_path in self.index_locations:
            try:
                # ディレクトリ作成
                index_path.parent.mkdir(parents=True, exist_ok=True)
                
                # インデックス保存
                with open(index_path, 'w') as f:
                    f.write(encrypted_index)
                
                os.chmod(index_path, 0o600)
                saved_count += 1
                
            except Exception as e:
                logger.warning(f"Failed to save index to {index_path}: {e}")
        
        # 少なくとも1箇所に保存できれば成功
        return saved_count > 0
    
    def _load_index(self) -> Optional[Dict]:
        """インデックス情報を読み込み"""
        for index_path in self.index_locations:
            try:
                if not index_path.exists():
                    continue
                
                with open(index_path, 'r') as f:
                    encrypted_index = f.read()
                
                index_data = json.loads(
                    self.persistent_encryption.decrypt(encrypted_index)
                )
                
                return index_data
                
            except Exception as e:
                logger.warning(f"Failed to load index from {index_path}: {e}")
        
        return None
    
    def _create_decoy_files(self, num_decoys: int = 20) -> None:
        """デコイファイルを生成"""
        for _ in range(num_decoys):
            try:
                # ランダムなセッションとファイル
                session_id = f"session-{secrets.token_hex(8)}"
                file_num = random.randint(1, 50)
                
                session_dir = self.base_path / session_id
                events_dir = session_dir / "events"
                events_dir.mkdir(parents=True, exist_ok=True)
                
                # ダミーイベント作成
                dummy_event = {
                    "id": file_num,
                    "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
                    "source": random.choice(["user", "agent", "system"]),
                    "action": random.choice(["message", "read", "write", "run"]),
                    "data": secrets.token_hex(32)  # ランダムデータ
                }
                
                file_path = events_dir / f"{file_num}.json"
                with open(file_path, 'w') as f:
                    json.dump(dummy_event, f, indent=2)
                    
            except Exception as e:
                logger.debug(f"Failed to create decoy: {e}")
    
    def _calculate_checksum(self, data: str) -> str:
        """チェックサムを計算"""
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _rollback_saves(self, locations: List[Dict]) -> None:
        """保存を巻き戻し"""
        for location in locations:
            self._delete_part(location)


# シングルトンインスタンス
_distributed_storage: Optional[DistributedStorage] = None


def get_distributed_storage() -> DistributedStorage:
    """分散ストレージのシングルトンインスタンスを取得"""
    global _distributed_storage
    if _distributed_storage is None:
        _distributed_storage = DistributedStorage()
    return _distributed_storage