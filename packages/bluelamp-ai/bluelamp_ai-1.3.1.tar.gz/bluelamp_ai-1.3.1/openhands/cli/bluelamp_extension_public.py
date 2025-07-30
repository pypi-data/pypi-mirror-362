#!/usr/bin/env python3
"""
BlueLamp Public CLI - Extension Manager Agent
一般公開用ブルーランプ拡張 - 拡張マネージャーエージェント
"""

import os
import sys

def main():
    """ブルーランプ拡張（拡張マネージャー）のメインエントリーポイント"""
    # 実行コマンドを識別するための環境変数
    os.environ['BLUELAMP_COMMAND'] = 'ブルーランプ拡張'
    
    # 現在のディレクトリをワークスペースとして設定
    current_dir = os.getcwd()
    os.environ['SANDBOX_VOLUMES'] = f"{current_dir}:/workspace:rw"
    
    # セッション情報を表示
    print("🔧エージェント：拡張マネージャー")
    print("ブルーランプ拡張モードを起動しています...")
    print("")
    
    # main_sessionモジュールをインポートして実行
    from openhands.cli.main_session.main import main as session_main
    session_main()

if __name__ == '__main__':
    main()