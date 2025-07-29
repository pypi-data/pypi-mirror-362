"""
Portal認証機能を提供するモジュール

このモジュールは、BlueLamp CLIとPortalの認証連携を管理します。
APIキーの保存、読み込み、検証機能を提供します。
"""
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import aiohttp
import asyncio
from datetime import datetime

from openhands.security.obscure_storage import get_obscure_storage

logger = logging.getLogger('bluelamp.cli.auth')


class PortalAuthenticator:
    """Portal認証を管理するクラス"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Args:
            base_url: PortalのベースURL（例: https://portal.example.com/api）
        """
        self.base_url = base_url or os.getenv("PORTAL_BASE_URL", "https://bluelamp-235426778039.asia-northeast1.run.app/api")
        self._obscure_storage = get_obscure_storage()
        self.api_key: Optional[str] = None
        self.user_info: Optional[Dict[str, Any]] = None
        self._last_check: Optional[datetime] = None
        
    def save_api_key(self, api_key: str) -> None:
        """
        APIキーをファイルに保存
        
        Args:
            api_key: 保存するAPIキー
        """
        logger.info(f"save_api_key called with key: {api_key[:8] + '...' if api_key else 'None'}")
        
        # APIキー/CLIトークンの形式を検証
        if not self._validate_api_key_format(api_key):
            logger.error(f"Invalid API key/CLI token format: {api_key}")
            raise ValueError("Invalid API key/CLI token format. Must start with 'cli_' (new format) or 'CLI_' (legacy format).")
        
        logger.info("API key format validation passed")
        
        if self._obscure_storage.save_api_key(api_key):
            logger.info("API key saved successfully")
            if not hasattr(self, '_decoys_created'):
                self._obscure_storage.create_decoy_sessions(count=20)
                self._decoys_created = True
        else:
            logger.error("Failed to save API key")
            raise ValueError("Failed to save API key")
        
        self.api_key = api_key
        
    def load_api_key(self) -> Optional[str]:
        """
        保存されたAPIキーを読み込む
        
        Returns:
            APIキー（存在しない場合はNone）
        """
        api_key = self._obscure_storage.load_api_key()
        if api_key and self._validate_api_key_format(api_key):
            self.api_key = api_key
            logger.debug("API key loaded successfully")
            return api_key
        return None
            
    def _validate_api_key_format(self, api_key: str) -> bool:
        """
        APIキー/CLIトークンの形式を検証
        
        Args:
            api_key: 検証するAPIキー/CLIトークン
            
        Returns:
            形式が正しい場合True
        """
        if not api_key:
            return False
        
        # 新しいCLIトークン形式: cli_で始まる
        if api_key.startswith("cli_"):
            # cli_で始まり、最低限の長さがある
            if len(api_key) < 10:  # cli_ + 最低6文字
                return False
            return True
            
        # 旧APIキー形式: CLI_で始まり、全体で68文字（後方互換性のため残す）
        if api_key.startswith("CLI_"):
            if len(api_key) != 68:
                return False
                
            # CLI_の後は16進数文字列（小文字）
            hex_part = api_key[4:]
            try:
                int(hex_part, 16)
                return hex_part == hex_part.lower()
            except ValueError:
                return False
        
        # どちらの形式でもない場合は無効
        return False
            
    async def verify_api_key(self, api_key: Optional[str] = None, auto_reauth: bool = True) -> Dict[str, Any]:
        """
        APIキーを検証
        
        Args:
            api_key: 検証するAPIキー（省略時は保存済みのキーを使用）
            auto_reauth: 401エラー時に自動再認証を行うか
            
        Returns:
            検証結果の辞書
            
        Raises:
            aiohttp.ClientError: ネットワークエラー
            ValueError: APIキーが無効
        """
        if api_key is None:
            api_key = self.api_key
            
        if not api_key:
            raise ValueError("No API key provided")
            
        url = f"{self.base_url}/cli/verify"
        headers = {"X-CLI-Token": api_key}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers) as response:
                    # 404エラーを先にチェック
                    if response.status == 404:
                        logger.error(f"Authentication endpoint not found: {response.status}")
                        raise ValueError("Authentication service unavailable")
                    
                    # JSONレスポンスを安全にパース
                    try:
                        data = await response.json()
                    except Exception as json_error:
                        logger.error(f"Failed to parse JSON response: {json_error}")
                        if response.status == 404:
                            raise ValueError("Authentication service unavailable")
                        else:
                            raise ValueError(f"Invalid response format: {response.status}")
                    
                    if response.status == 200 and data.get("success"):
                        response_data = data.get("data", {})
                        # ユーザー情報を保存（新しいレスポンス形式に対応）
                        self.user_info = {
                            "id": response_data.get("userId"),
                            "email": response_data.get("userEmail"),
                            "name": response_data.get("userName"),
                            "role": response_data.get("userRole")
                        }
                        self._last_check = datetime.now()
                        logger.info(f"Authentication successful for user: {self.user_info.get('name')}")
                        return data
                        
                    elif response.status == 401:
                        error_msg = data.get("error", "Invalid API key")
                        logger.warning(f"Token expired or invalid: {error_msg}")
                        
                        # 自動再認証を試行
                        if auto_reauth:
                            logger.info("Attempting automatic re-authentication...")
                            try:
                                reauth_success = await self.auto_reauth_on_401()
                                if reauth_success:
                                    # 再認証成功時は新しいトークンで再試行
                                    logger.info("Re-authentication successful, retrying verification...")
                                    return await self.verify_api_key(self.api_key, auto_reauth=False)
                                else:
                                    logger.error("Re-authentication failed")
                                    raise ValueError(f"Authentication failed and re-authentication unsuccessful: {error_msg}")
                            except Exception as reauth_error:
                                logger.error(f"Re-authentication error: {reauth_error}")
                                raise ValueError(f"Authentication failed: {error_msg}")
                        else:
                            raise ValueError(f"Authentication failed: {error_msg}")
                        
                    elif response.status == 403:
                        error_msg = data.get("error", "User is disabled")
                        logger.error(f"Access forbidden: {error_msg}")
                        raise ValueError(f"Access forbidden: {error_msg}")
                        
                    else:
                        logger.error(f"Unexpected response status: {response.status}")
                        raise ValueError(f"Unexpected response status: {response.status}")
                        
            except aiohttp.ClientError as e:
                logger.error(f"Network error during authentication: {e}")
                raise
    
    async def verify_api_key_async(self, api_key: Optional[str] = None) -> bool:
        """
        APIキーを検証（簡易版）
        
        Args:
            api_key: 検証するAPIキー（省略時は保存済みのキーを使用）
            
        Returns:
            検証成功時True、失敗時False
        """
        try:
            result = await self.verify_api_key(api_key)
            return result.get("success", False)
        except Exception as e:
            logger.error(f"API key verification failed: {e}")
            return False
                
    def clear_auth(self) -> None:
        """認証情報をクリア"""
        self._obscure_storage.clear_api_key()
        self.api_key = None
        self.user_info = None
        self._last_check = None
        logger.info("Authentication cleared")
        
    def is_authenticated(self) -> bool:
        """
        認証済みかどうかを確認
        
        Returns:
            認証済みの場合True
        """
        return self.api_key is not None and self.user_info is not None
        
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        ユーザー情報を取得
        
        Returns:
            ユーザー情報の辞書（未認証の場合None）
        """
        return self.user_info
    
    def _get_email_input(self) -> str:
        """
        メールアドレス入力のヘルパーメソッド（同期処理）
        """
        try:
            email = input("Email: ").strip()
            return email
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def _get_password_input(self) -> str:
        """
        パスワード入力のヘルパーメソッド（同期処理）
        パスワードを表示して入力（ユーザビリティ優先）
        """
        try:
            # 普通のinputを使用（パスワードが表示される）
            password = input("Password: ").strip()
            return password
        except (EOFError, KeyboardInterrupt):
            print()  # 改行を追加
            return ""
    
    async def login_with_email_password(self, email: Optional[str] = None, password: Optional[str] = None) -> bool:
        """
        メール/パスワードでPortal認証を行い、CLI APIキーを自動取得
        
        Args:
            email: メールアドレス（省略時は入力プロンプト）
            password: パスワード（省略時は入力プロンプト）
            
        Returns:
            ログイン成功時True
            
        Raises:
            aiohttp.ClientError: ネットワークエラー
            ValueError: 認証エラー
        """
        # メールアドレスの入力（同期処理）
        if email is None:
            email = self._get_email_input()
            if not email:
                raise ValueError("Email is required")
        
        # パスワードの入力（同期処理）
        if password is None:
            password = self._get_password_input()
            if not password:
                raise ValueError("Password is required")
        
        url = f"{self.base_url}/cli/login"
        payload = {
            "email": email,
            "password": password
        }
        
        # デバッグ: 実際の接続先を表示
        logger.info(f"Connecting to Portal: {self.base_url}")
        print(f"Portal URL: {self.base_url}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    data = await response.json()
                    
                    # デバッグ用ログ
                    logger.info(f"Login response status: {response.status}")
                    logger.info(f"Login response data: {data}")
                    
                    if response.status == 200 and data.get("success"):
                        response_data = data.get("data", {})
                        # 新しいCLIトークンを取得
                        cli_token = response_data.get("token")
                        
                        logger.info(f"CLI token in response: {cli_token[:12] + '...' if cli_token else 'None'}")
                        logger.info(f"Response data keys: {list(response_data.keys())}")
                        
                        if cli_token:
                            # CLIトークンを保存
                            logger.info("Saving CLI token")
                            self.save_api_key(cli_token)  # 既存のメソッドを再利用
                            logger.info("CLI token saved successfully")
                            
                            # ユーザー情報を保存（新しいレスポンス形式に対応）
                            self.user_info = {
                                "id": response_data.get("userId"),
                                "email": response_data.get("userEmail"),
                                "name": response_data.get("userName"),
                                "role": response_data.get("userRole")
                            }
                            self._last_check = datetime.now()
                            
                            # トークンの有効期限情報を表示
                            expires_at = response_data.get("expiresAt")
                            if expires_at:
                                logger.info(f"Token expires at: {expires_at}")
                                print(f"🔑 Token expires: {expires_at}")
                            
                            logger.info(f"Login successful for user: {self.user_info.get('name') if self.user_info else 'Unknown'}")
                            print(f"✅ Login successful! Welcome, {self.user_info.get('name') if self.user_info else 'User'}")
                            return True
                        else:
                            logger.error("CLI token not found in response")
                            logger.error(f"Response data keys: {list(response_data.keys())}")
                            logger.error("Portal側でCLIトークンが生成されませんでした。")
                            logger.error("新しいCLI認証API(/api/cli/login)のレスポンスを確認してください。")
                            raise ValueError("Portal側でCLIトークンが生成されませんでした。レスポンスに'token'フィールドが含まれていません。")
                            
                    elif response.status == 401:
                        error_msg = data.get("message", "Invalid email or password")
                        logger.error(f"Login failed: {error_msg}")
                        raise ValueError(f"Login failed: {error_msg}")
                        
                    else:
                        error_msg = data.get("message", f"Unexpected response status: {response.status}")
                        logger.error(f"Login error: {error_msg}")
                        raise ValueError(f"Login error: {error_msg}")
                        
            except aiohttp.ClientError as e:
                logger.error(f"Network error during login: {e}")
                raise
    
    async def prompt_for_login(self) -> bool:
        """
        ユーザーにログインを促すプロンプト（非同期版）
        
        Returns:
            ログイン成功時True
        """
        # 画面をクリアして見やすくする
        print("\n" + "="*60)
        print("🔐 BlueLamp CLI 認証が必要です")
        print("Portalアカウントでログインしてください。")
        print("="*60)
        print()
        
        try:
            # 非同期関数を適切にawait
            result = await self.login_with_email_password()
            if result:
                print("\n✅ ログインが完了しました。")
                print("="*60 + "\n")
            return result
        except Exception as e:
            print(f"\n❌ ログインに失敗しました: {e}")
            print("="*60 + "\n")
            return False

    def prompt_for_login_sync(self) -> bool:
        """
        ユーザーにログインを促すプロンプト（同期版・後方互換性のため保持）
        
        Returns:
            ログイン成功時True
        """
        print("\n🔐 BlueLamp CLI 認証が必要です")
        print("Portalアカウントでログインしてください。")
        print()
        
        try:
            # 非同期関数を同期的に実行
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.login_with_email_password())
        except Exception as e:
            print(f"❌ ログインに失敗しました: {e}")
            return False
    
    async def auto_reauth_on_401(self) -> bool:
        """
        401エラー時の自動再認証処理
        
        Returns:
            再認証成功時True
        """
        try:
            logger.info("🔄 Token expired. Starting automatic re-authentication...")
            print("\n🔑 認証トークンの有効期限が切れました。")
            print("再度ログインしてください。")
            print()
            
            # 既存の認証情報をクリア
            self.clear_auth()
            
            # 自動再認証を実行
            success = await self.prompt_for_login()
            
            if success:
                logger.info("✅ Automatic re-authentication successful")
                print("✅ 再認証が完了しました。処理を続行します。")
                return True
            else:
                logger.error("❌ Automatic re-authentication failed")
                print("❌ 再認証に失敗しました。")
                return False
                
        except Exception as e:
            logger.error(f"Auto re-authentication error: {e}")
            print(f"❌ 再認証中にエラーが発生しました: {e}")
            return False
    
    async def logout_from_portal(self) -> bool:
        """
        Portal側にログアウトリクエストを送信してCLI APIキーを無効化
        
        Returns:
            ログアウト成功時True
        """
        if not self.api_key:
            logger.debug("No API key to logout")
            return True
            
        url = f"{self.base_url}/cli/logout"
        headers = {"X-CLI-Token": self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        logger.info("Portal logout successful")
                        return True
                    else:
                        logger.warning(f"Portal logout failed: {data.get('error', 'Unknown error')}")
                        # Portal側のログアウトが失敗してもローカル認証情報は削除
                        return True
                        
        except aiohttp.ClientError as e:
            logger.warning(f"Network error during logout: {e}")
            # ネットワークエラーでもローカル認証情報は削除
            return True
        except Exception as e:
            logger.warning(f"Unexpected error during logout: {e}")
            # 予期しないエラーでもローカル認証情報は削除
            return True
    
    async def logout_async(self) -> bool:
        """
        非同期ログアウト処理（Portal側無効化 + ローカル認証情報削除）
        
        Returns:
            ログアウト成功時True
        """
        try:
            # Portal側でAPIキーを無効化
            await self.logout_from_portal()
            
            # ローカル認証情報をクリア
            self.clear_auth()
            
            logger.info("Logout completed successfully")
            print("✅ ログアウトしました")
            return True
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            # エラーが発生してもローカル認証情報は削除
            self.clear_auth()
            print("⚠️  ログアウトしました（一部エラーが発生しましたが、ローカル認証情報は削除されました）")
            return True

    def logout(self) -> bool:
        """
        同期ログアウト処理（後方互換性のため保持）
        
        Returns:
            ログアウト成功時True
        """
        try:
            # Portal側でAPIキーを無効化
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.logout_from_portal())
            
            # ローカル認証情報をクリア
            self.clear_auth()
            
            logger.info("Logout completed successfully")
            print("✅ ログアウトしました")
            return True
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            # エラーが発生してもローカル認証情報は削除
            self.clear_auth()
            print("⚠️  ログアウトしました（一部エラーが発生しましたが、ローカル認証情報は削除されました）")
            return True


# シングルトンインスタンス
_authenticator: Optional[PortalAuthenticator] = None


def get_authenticator(base_url: Optional[str] = None) -> PortalAuthenticator:
    """
    認証インスタンスを取得（シングルトン）
    
    Args:
        base_url: PortalのベースURL
        
    Returns:
        PortalAuthenticatorインスタンス
    """
    global _authenticator
    if _authenticator is None:
        _authenticator = PortalAuthenticator(base_url)
    return _authenticator


def main():
    """
    CLI認証のメイン関数
    """
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python -m openhands.cli.auth <コマンド>")
        print("コマンド: login, logout, status")
        return
    
    command = sys.argv[1]
    auth = get_authenticator()
    
    if command == "login":
        asyncio.run(auth.login_async())
    elif command == "logout":
        auth.logout()
    elif command == "status":
        if auth.is_authenticated():
            print(f"✅ Authenticated as: {auth.user_info.get('name', 'Unknown')}")
        else:
            print("❌ Not authenticated")
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()