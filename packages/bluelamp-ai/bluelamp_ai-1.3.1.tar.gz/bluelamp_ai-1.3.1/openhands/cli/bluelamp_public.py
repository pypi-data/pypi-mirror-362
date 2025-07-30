#!/usr/bin/env python3
"""
BlueLamp Public CLI - Orchestrator Agent
一般公開用ブルーランプ - オーケストレーターエージェント
"""

import os
import sys

def main():
    """ブルーランプ（オーケストレーター）のメインエントリーポイント"""
    # 実行コマンドを識別するための環境変数
    os.environ['BLUELAMP_COMMAND'] = 'ブルーランプ'
    
    # 現在のディレクトリをワークスペースとして設定
    current_dir = os.getcwd()
    os.environ['SANDBOX_VOLUMES'] = f"{current_dir}:/workspace:rw"
    
    # セッション情報を表示
    print("🔵エージェント：オーケストレーター")
    print("ブルーランプを起動しています...")
    print("")
    
    # main_sessionモジュールをインポートして実行
    from openhands.cli.main_session.main import main as session_main
    session_main()

if __name__ == '__main__':
    main()