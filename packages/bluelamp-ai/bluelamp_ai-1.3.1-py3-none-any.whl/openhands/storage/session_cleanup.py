"""
セッション自動削除機能

問題：
- 991個のセッションフォルダが蓄積（1.4GB）
- 自動削除機能なし
- ディスク容量圧迫

解決策：
- 古いセッションの自動削除
- 設定可能な保持期間
- 安全な削除処理
"""

import os
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from openhands.core.logger import openhands_logger as logger


class SessionCleanup:
    """セッション自動削除管理クラス"""
    
    def __init__(self, sessions_dir: str = "~/.openhands/sessions"):
        self.sessions_dir = Path(sessions_dir).expanduser()
        
    def get_session_age_days(self, session_path: Path) -> float:
        """セッションの経過日数を取得"""
        try:
            # セッションフォルダの作成時刻を取得
            creation_time = session_path.stat().st_ctime
            age_seconds = time.time() - creation_time
            return age_seconds / (24 * 60 * 60)  # 日数に変換
        except Exception as e:
            logger.warning(f"セッション年齢取得エラー {session_path}: {e}")
            return 0
    
    def get_session_size_mb(self, session_path: Path) -> float:
        """セッションのサイズ（MB）を取得"""
        try:
            total_size = 0
            for file_path in session_path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size / (1024 * 1024)  # MBに変換
        except Exception as e:
            logger.warning(f"セッションサイズ取得エラー {session_path}: {e}")
            return 0
    
    def list_old_sessions(self, max_age_days: int = 7) -> list[tuple[Path, float, float]]:
        """古いセッションのリストを取得"""
        old_sessions = []
        
        if not self.sessions_dir.exists():
            return old_sessions
            
        for session_path in self.sessions_dir.iterdir():
            if not session_path.is_dir():
                continue
                
            age_days = self.get_session_age_days(session_path)
            size_mb = self.get_session_size_mb(session_path)
            
            if age_days > max_age_days:
                old_sessions.append((session_path, age_days, size_mb))
        
        # 古い順にソート
        old_sessions.sort(key=lambda x: x[1], reverse=True)
        return old_sessions
    
    def cleanup_old_sessions(
        self, 
        max_age_days: int = 7, 
        dry_run: bool = True,
        max_delete_count: Optional[int] = None
    ) -> dict:
        """古いセッションを削除"""
        old_sessions = self.list_old_sessions(max_age_days)
        
        if max_delete_count:
            old_sessions = old_sessions[:max_delete_count]
        
        deleted_count = 0
        deleted_size_mb = 0
        errors = []
        
        for session_path, age_days, size_mb in old_sessions:
            try:
                if dry_run:
                    logger.info(f"[DRY RUN] 削除対象: {session_path.name} ({age_days:.1f}日前, {size_mb:.1f}MB)")
                else:
                    logger.info(f"削除実行: {session_path.name} ({age_days:.1f}日前, {size_mb:.1f}MB)")
                    shutil.rmtree(session_path)
                    
                deleted_count += 1
                deleted_size_mb += size_mb
                
            except Exception as e:
                error_msg = f"削除エラー {session_path.name}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        return {
            "deleted_count": deleted_count,
            "deleted_size_mb": deleted_size_mb,
            "total_sessions": len(old_sessions),
            "errors": errors,
            "dry_run": dry_run
        }
    
    def get_sessions_summary(self) -> dict:
        """セッション統計情報を取得"""
        if not self.sessions_dir.exists():
            return {"total_sessions": 0, "total_size_mb": 0}
            
        total_sessions = 0
        total_size_mb = 0
        
        for session_path in self.sessions_dir.iterdir():
            if session_path.is_dir():
                total_sessions += 1
                total_size_mb += self.get_session_size_mb(session_path)
        
        return {
            "total_sessions": total_sessions,
            "total_size_mb": total_size_mb,
            "total_size_gb": total_size_mb / 1024
        }


def auto_cleanup_sessions(
    max_age_days: int = 7,
    dry_run: bool = True,
    max_delete_count: Optional[int] = 100
) -> dict:
    """セッション自動削除のメイン関数"""
    cleanup = SessionCleanup()
    
    # 現在の統計
    summary = cleanup.get_sessions_summary()
    logger.info(f"セッション統計: {summary['total_sessions']}個, {summary['total_size_gb']:.2f}GB")
    
    # 古いセッションの削除
    result = cleanup.cleanup_old_sessions(
        max_age_days=max_age_days,
        dry_run=dry_run,
        max_delete_count=max_delete_count
    )
    
    if result["deleted_count"] > 0:
        logger.info(
            f"削除{'予定' if dry_run else '完了'}: "
            f"{result['deleted_count']}個のセッション, "
            f"{result['deleted_size_mb']:.1f}MB"
        )
    
    return result


if __name__ == "__main__":
    # テスト実行
    print("=== セッション削除テスト（DRY RUN） ===")
    result = auto_cleanup_sessions(max_age_days=7, dry_run=True, max_delete_count=10)
    print(f"結果: {result}")