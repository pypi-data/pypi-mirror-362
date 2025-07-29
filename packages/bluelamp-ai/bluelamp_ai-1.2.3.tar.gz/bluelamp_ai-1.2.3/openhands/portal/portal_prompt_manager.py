"""
Portal連携PromptManager
Portal APIからプロンプトを取得する専用クラス
"""
import os
import asyncio
import logging
from typing import Optional, TYPE_CHECKING

from .prompt_client import PortalPromptClient
from .prompt_mapping import is_portal_prompt
from openhands.utils.prompt import PromptManager

if TYPE_CHECKING:
    from openhands.controller.state.state import State
    from openhands.core.message import Message

logger = logging.getLogger('bluelamp.portal.prompt_manager')


class PortalPromptManager(PromptManager):
    """Portal APIからプロンプトを取得する専用クラス"""
    
    def __init__(
        self,
        prompt_dir: str,
        system_prompt_filename: str = 'system_prompt.j2',
        portal_base_url: Optional[str] = None,
        enable_portal: bool = True
    ):
        """
        Args:
            prompt_dir: プロンプトディレクトリ
            system_prompt_filename: システムプロンプトファイル名
            portal_base_url: PortalのベースURL
            enable_portal: Portal連携を有効にするか
        """
        # エージェント名を抽出
        agent_name = self._extract_agent_name(system_prompt_filename)
        
        # Portal専用エージェントの場合は親クラスの初期化をスキップ
        if enable_portal and agent_name and is_portal_prompt(agent_name):
            # 親クラスの属性を直接設定（ローカルファイル読み込みをスキップ）
            self.prompt_dir = prompt_dir
            self.system_template = None  # type: ignore
            self.user_template = None  # type: ignore
            self.additional_info_template = None  # type: ignore
        else:
            # 通常のローカルファイル処理
            super().__init__(prompt_dir, system_prompt_filename)
        
        # Portal固有の設定
        self.system_prompt_filename = system_prompt_filename
        self.portal_client = PortalPromptClient(base_url=portal_base_url) if enable_portal else None
        self.enable_portal = enable_portal
        self._portal_content_cache: Optional[str] = None
        
        logger.info(f"PortalPromptManager初期化: portal={enable_portal}, file={system_prompt_filename}")
    
    def _extract_agent_name(self, filename: str) -> Optional[str]:
        """ファイル名からエージェント名を抽出"""
        if filename.endswith('_system_prompt.j2'):
            return filename.replace('_system_prompt.j2', '')
        elif filename == 'system_prompt.j2':
            # デフォルトのsystem_prompt.j2の場合、ディレクトリ名からエージェント名を推測
            agent_name = os.path.basename(self.prompt_dir)
            return agent_name if agent_name else None
        elif '.' not in filename:
            # 拡張子がない場合はそのままエージェント名として扱う
            return filename
        return None
    
    async def _fetch_portal_content(self, retry_on_auth_error: bool = True) -> Optional[str]:
        """Portal APIからプロンプト内容を取得"""
        if not self.enable_portal or not self.portal_client:
            return None
            
        try:
            # Portal連携対象かチェック
            agent_name = self._extract_agent_name(self.system_prompt_filename)
            if not agent_name or not is_portal_prompt(agent_name):
                logger.debug(f"Portal連携対象外: {self.system_prompt_filename}")
                return None
            
            # 既存の認証システムを活用（認証エラー時は自動ログイン画面へ）
            if retry_on_auth_error:
                from openhands.cli.auth import PortalAuthenticator
                authenticator = PortalAuthenticator()
                authenticator.load_api_key()  # APIキーを読み込み
                
                # APIキーが存在しない場合は直接ログインを促す
                if not authenticator.api_key:
                    logger.info("APIキーが見つかりません。ログインを開始します...")
                    login_success = await authenticator.prompt_for_login()
                    if not login_success:
                        logger.warning("ログインがキャンセルされました")
                        return None
                else:
                    # APIキー検証（自動再認証機能付き）
                    try:
                        verification_result = await authenticator.verify_api_key(auto_reauth=True)
                        if not verification_result.get('success', False):
                            logger.warning("Portal認証に失敗しました")
                            return None
                    except ValueError as e:
                        if "No API key provided" in str(e):
                            # APIキーがない場合はログインを促す
                            logger.info("APIキーが無効です。ログインを開始します...")
                            login_success = await authenticator.prompt_for_login()
                            if not login_success:
                                logger.warning("ログインがキャンセルされました")
                                return None
                        else:
                            logger.error(f"認証エラー: {e}")
                            return None
            
            # エージェント名を使ってPortal APIから取得
            content = await self.portal_client.fetch_prompt_by_agent_name(agent_name)
            if content:
                logger.info(f"Portal プロンプト取得成功: {agent_name}")
                return content
            else:
                logger.warning(f"Portal プロンプト取得失敗: {agent_name}")
                return None
                
        except Exception as e:
            logger.error(f"Portal プロンプト取得エラー: {e}")
            return None
    
    def get_system_message(self) -> str:
        """Portal APIからシステムメッセージを取得"""
        try:
            logger.info(f"[PortalPromptManager] get_system_message called with filename: {self.system_prompt_filename}")
            
            # キャッシュがある場合はそれを使用
            if self._portal_content_cache is not None:
                logger.debug("キャッシュからプロンプトを返却")
                return self._clean_portal_prompt(self._portal_content_cache)
            
            # Portal連携が有効で対象ファイルの場合
            if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
                try:
                    # 非同期処理を同期的に実行
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # 既にイベントループが動いている場合は新しいタスクとして実行
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(asyncio.run, self._fetch_portal_content())
                            portal_content = future.result(timeout=10)
                    else:
                        # イベントループが動いていない場合は直接実行
                        portal_content = asyncio.run(self._fetch_portal_content())
                    
                    if portal_content:
                        self._portal_content_cache = portal_content
                        logger.info(f"Portal プロンプト使用: {self.system_prompt_filename}")
                        # プロンプトの内容を一部ログ出力
                        preview = portal_content[:200] if len(portal_content) > 200 else portal_content
                        logger.info(f"Portal プロンプト内容プレビュー: {preview}...")
                        return self._clean_portal_prompt(portal_content)
                        
                except Exception as e:
                    logger.warning(f"Portal プロンプト取得失敗: {e}")
            
            # デフォルトプロンプトを返す
            logger.info("デフォルトプロンプトを使用")
            return "# System Prompt\nYou are a helpful AI assistant."
            
        except Exception as e:
            logger.error(f"プロンプト取得エラー: {e}")
            return "# System Prompt\nYou are a helpful AI assistant."
    
    async def get_system_message_async(self) -> str:
        """非同期でシステムメッセージを取得"""
        try:
            # キャッシュがある場合はそれを使用
            if self._portal_content_cache is not None:
                logger.debug("キャッシュからプロンプトを返却")
                return self._clean_portal_prompt(self._portal_content_cache)
            
            # Portal連携が有効で対象ファイルの場合
            if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
                portal_content = await self._fetch_portal_content()
                if portal_content:
                    self._portal_content_cache = portal_content
                    logger.info(f"Portal プロンプト使用: {self.system_prompt_filename}")
                    return self._clean_portal_prompt(portal_content)
            
            # デフォルトプロンプトを返す
            logger.info("デフォルトプロンプトを使用")
            return "# System Prompt\nYou are a helpful AI assistant."
            
        except Exception as e:
            logger.error(f"プロンプト取得エラー: {e}")
            return "# System Prompt\nYou are a helpful AI assistant."
    
    def _clean_portal_prompt(self, content: str) -> str:
        """
        Portalから取得したプロンプトをクリーンアップ
        - メタデータ（Source、Fetchedなど）を削除
        - {{ instructions }}などのテンプレート変数を処理
        """
        try:
            # "---"で始まるメタデータセクションを削除
            if "\n---\n" in content:
                content = content.split("\n---\n")[0]
            
            # {{ instructions }}を空文字に置換（必要に応じて後で実装）
            content = content.replace("{{ instructions }}", "")
            
            return content.strip()
        except Exception as e:
            logger.error(f"プロンプトクリーンアップエラー: {e}")
            return content
    
    def clear_cache(self):
        """プロンプトキャッシュをクリア"""
        self._portal_content_cache = None
        logger.debug("プロンプトキャッシュをクリアしました")
    
    async def test_portal_connection(self) -> bool:
        """Portal接続テスト"""
        if not self.enable_portal or not self.portal_client:
            return False
        return await self.portal_client.test_connection()
    
    def get_example_user_message(self) -> str:
        """ユーザーメッセージ例を取得"""
        if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
            return ""  # Portal専用ファイルの場合は空文字
        return super().get_example_user_message()
    
    def get_user_message(self, task: str, **kwargs) -> str:
        """ユーザーメッセージを取得"""
        if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
            return task  # Portal専用ファイルの場合はタスクをそのまま返す
        return super().get_user_message(task, **kwargs)
    
    def build_workspace_context(
        self,
        repository_info=None,
        runtime_info=None,
        conversation_instructions=None,
        repo_instructions: str = '',
    ) -> str:
        """ワークスペースコンテキストを構築"""
        if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
            return ""  # Portal専用ファイルの場合は空文字
        return super().build_workspace_context(
            repository_info=repository_info,
            runtime_info=runtime_info,
            conversation_instructions=conversation_instructions,
            repo_instructions=repo_instructions,
        )
    
    
    def add_turns_left_reminder(self, messages: list['Message'], state: 'State') -> None:
        """残りターン数のリマインダーをメッセージに追加"""
        if self.enable_portal and is_portal_prompt(self.system_prompt_filename):
            pass  # Portal専用ファイルの場合は何もしない
        else:
            super().add_turns_left_reminder(messages, state)


# 便利関数
def create_portal_prompt_manager(
    prompt_dir: str,
    system_prompt_filename: str = 'system_prompt.j2',
    portal_base_url: Optional[str] = None,
    enable_portal: bool = True
) -> PortalPromptManager:
    """PortalPromptManagerを作成する便利関数"""
    return PortalPromptManager(
        prompt_dir=prompt_dir,
        system_prompt_filename=system_prompt_filename,
        portal_base_url=portal_base_url,
        enable_portal=enable_portal
    )


