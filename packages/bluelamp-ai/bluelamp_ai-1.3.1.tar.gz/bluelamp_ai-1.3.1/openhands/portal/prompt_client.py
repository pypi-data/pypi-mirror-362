"""
Portal プロンプトクライアント
Portal APIからプロンプトを取得するクライアント
"""
import os
import json
import logging
import asyncio
from typing import Optional, Dict, Any
from pathlib import Path
import aiohttp

from .prompt_mapping import get_prompt_id, get_prompt_title, get_agent_name
from openhands.security.obscure_storage import get_obscure_storage

logger = logging.getLogger('bluelamp.portal.prompt_client')


class PortalPromptClient:
    """Portal からプロンプトを取得するクライアント"""
    
    def __init__(self, base_url: Optional[str] = None, auth_file: Optional[Path] = None):
        """
        Args:
            base_url: PortalのベースURL
            auth_file: 認証情報ファイルのパス
        """
        self.base_url = base_url or os.getenv("PORTAL_BASE_URL", "http://bluelamp-235426778039.asia-northeast1.run.app/api")
        self._obscure_storage = get_obscure_storage()
        self._api_key: Optional[str] = None
        
    def _load_api_key(self) -> Optional[str]:
        """認証ファイルからAPIキーを読み込み"""
        try:
            api_key = self._obscure_storage.load_api_key()
            if api_key:
                logger.debug("APIキーを読み込みました")
                return api_key
        except Exception as e:
            logger.error(f"APIキー読み込みエラー: {e}")
        return None
    
    async def fetch_prompt(self, prompt_id: str) -> Optional[str]:
        """
        Portal APIからプロンプトを取得
        
        Args:
            prompt_id: Portal側のプロンプトID
            
        Returns:
            プロンプト内容（文字列）またはNone
        """
        try:
            # APIキーを取得
            if not self._api_key:
                self._api_key = self._load_api_key()
                
            if not self._api_key:
                logger.error("APIキーが取得できません")
                return None
            
            # APIエンドポイント
            url = f"{self.base_url}/cli/prompts/{prompt_id}"
            
            # ヘッダー設定
            headers = {
                'X-CLI-Token': self._api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'BlueLamp-CLI/1.0'
            }
            
            logger.debug(f"プロンプト取得開始: {prompt_id} ({get_prompt_title(prompt_id)})")
            
            # API呼び出し
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:  # type: ignore
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('success') and 'data' in data:
                            prompt_content = data['data']['prompt']['content']
                            logger.info(f"プロンプト取得成功: {prompt_id}")
                            return prompt_content
                        else:
                            logger.error(f"APIレスポンス形式エラー: {data}")
                            return None
                            
                    elif response.status == 401:
                        logger.error("認証エラー: APIキーが無効または期限切れです")
                        return None
                        
                    elif response.status == 404:
                        logger.error(f"プロンプトが見つかりません: {prompt_id}")
                        return None
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"API呼び出しエラー: {response.status} - {error_text}")
                        return None
                        
        except asyncio.TimeoutError:
            logger.error(f"プロンプト取得タイムアウト: {prompt_id}")
            return None
            
        except Exception as e:
            logger.error(f"プロンプト取得エラー: {e}")
            return None
    
    async def fetch_prompt_by_agent_name(self, agent_name: str) -> Optional[str]:
        """
        エージェント名からプロンプトを取得
        
        Args:
            agent_name: エージェント名（例: 'orchestrator', 'requirements_engineer'）
            
        Returns:
            プロンプト内容（文字列）またはNone
        """
        prompt_id = get_prompt_id(agent_name)
        if not prompt_id:
            logger.warning(f"Portal連携対象外のエージェント: {agent_name}")
            return None
            
        return await self.fetch_prompt(prompt_id)
    
    async def test_connection(self) -> bool:
        """
        Portal接続テスト
        
        Returns:
            接続成功の場合True
        """
        try:
            # テスト用に機能拡張プランナーのプロンプトを取得
            test_prompt_id = get_prompt_id('feature_extension.j2')
            if not test_prompt_id:
                logger.error("テスト用プロンプトIDが見つかりません")
                return False
                
            result = await self.fetch_prompt(test_prompt_id)
            if result:
                logger.info("Portal接続テスト成功")
                return True
            else:
                logger.error("Portal接続テスト失敗")
                return False
                
        except Exception as e:
            logger.error(f"Portal接続テストエラー: {e}")
            return False
    
    async def get_available_prompts(self) -> Dict[str, str]:
        """
        利用可能なプロンプト一覧を取得
        
        Returns:
            {agent_name: prompt_id} の辞書
        """
        try:
            # APIキーを取得
            if not self._api_key:
                self._api_key = self._load_api_key()
                
            if not self._api_key:
                logger.error("APIキーが取得できません")
                return {}
            
            # APIエンドポイント
            url = f"{self.base_url}/cli/prompts"
            
            # ヘッダー設定
            headers = {
                'X-CLI-Token': self._api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'BlueLamp-CLI/1.0'
            }
            
            logger.debug("利用可能プロンプト一覧取得開始")
            
            # API呼び出し
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:  # type: ignore
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('success') and 'data' in data:
                            prompts = data['data']['prompts']
                            result = {}
                            
                            for prompt in prompts:
                                prompt_id = prompt['id']
                                agent_name = get_agent_name(prompt_id)
                                if agent_name:
                                    result[agent_name] = prompt_id
                                    
                            logger.info(f"利用可能プロンプト一覧取得成功: {len(result)}件")
                            return result
                        else:
                            logger.error(f"APIレスポンス形式エラー: {data}")
                            return {}
                            
                    else:
                        error_text = await response.text()
                        logger.error(f"API呼び出しエラー: {response.status} - {error_text}")
                        return {}
                        
        except Exception as e:
            logger.error(f"利用可能プロンプト一覧取得エラー: {e}")
            return {}


# 便利関数
async def fetch_portal_prompt(agent_name: str, base_url: Optional[str] = None) -> Optional[str]:
    """
    エージェント名からPortalプロンプトを取得する便利関数
    
    Args:
        agent_name: エージェント名
        base_url: PortalのベースURL（オプション）
        
    Returns:
        プロンプト内容またはNone
    """
    client = PortalPromptClient(base_url=base_url)
    return await client.fetch_prompt_by_agent_name(agent_name)


# テスト用関数
async def test_portal_connection(base_url: Optional[str] = None) -> bool:
    """Portal接続テスト用関数"""
    client = PortalPromptClient(base_url=base_url)
    return await client.test_connection()


if __name__ == "__main__":
    # テスト実行
    async def main():
        client = PortalPromptClient()
        
        # 接続テスト
        print("Portal接続テスト...")
        if await client.test_connection():
            print("✅ 接続成功")
        else:
            print("❌ 接続失敗")
            return
        
        # プロンプト取得テスト
        print("\nプロンプト取得テスト...")
        content = await client.fetch_prompt_by_agent_name('feature_extension')
        if content:
            print(f"✅ プロンプト取得成功: {len(content)}文字")
            print(f"内容プレビュー: {content[:100]}...")
        else:
            print("❌ プロンプト取得失敗")
    
    asyncio.run(main())