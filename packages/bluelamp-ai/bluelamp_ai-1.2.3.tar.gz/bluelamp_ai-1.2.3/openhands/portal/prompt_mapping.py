"""
プロンプトマッピング設定
エージェント名とPortal側プロンプトIDのマッピング（14エージェント構造）
Portal APIのみを使用し、ローカル.j2ファイルは使用しません
"""

# エージェント名 → Portal プロンプトID (14エージェント構造: 00-13)
PROMPT_MAPPING = {
    # 00: オーケストレーター (OrchestratorAgent用)
    'orchestrator': '6862397f1428c1efc592f6cc',
    # 01: 要件定義エンジニア
    'requirements_engineer': '6862397f1428c1efc592f6ce',
    # 02: UIUXデザイナー
    'uiux_designer': '6862397f1428c1efc592f6d0',
    # 03: データモデリングエンジニア
    'data_modeling_engineer': '6862397f1428c1efc592f6d2',
    # 04: システムアーキテクト
    'system_architect': '6862397f1428c1efc592f6d4',
    # 05: 実装コンサルタント
    'implementation_consultant': '6862397f1428c1efc592f6d6',
    # 06: 環境構築
    'environment_setup': '6862397f1428c1efc592f6d8',
    # 07: PRC実装エージェント
    'prc_implementation': '6862397f1428c1efc592f6da',
    # 08: デバッグエージェント
    'debug_agent': '6862397f1428c1efc592f6dc',
    # 09: デプロイスペシャリスト
    'deploy_specialist': '6862397f1428c1efc592f6de',
    # 10: 拡張オーケストレーター (ExtensionManagerAgent用)
    'expansion_orchestrator': '6862397f1428c1efc592f6e0',
    # 11: 新ページ作成エージェント
    'page_creator': '6862397f1428c1efc592f6e2',
    # 12: リファクタリング計画エージェント
    'refactoring_planner': '6862397f1428c1efc592f6e4',
    # 13: リファクタリング実装エージェント
    'refactoring_implementation': '6862397f1428c1efc592f6e6',
}

# 逆マッピング（プロンプトID → エージェント名）
ID_TO_AGENT = {v: k for k, v in PROMPT_MAPPING.items()}

# プロンプトタイトルマッピング（デバッグ用）- 14エージェント構造
PROMPT_TITLES = {
    '6862397f1428c1efc592f6cc': '00: オーケストレーター',
    '6862397f1428c1efc592f6ce': '01: 要件定義エンジニア',
    '6862397f1428c1efc592f6d0': '02: UIUXデザイナー',
    '6862397f1428c1efc592f6d2': '03: データモデリングエンジニア',
    '6862397f1428c1efc592f6d4': '04: システムアーキテクト',
    '6862397f1428c1efc592f6d6': '05: 実装コンサルタント',
    '6862397f1428c1efc592f6d8': '06: 環境構築',
    '6862397f1428c1efc592f6da': '07: PRC実装エージェント',
    '6862397f1428c1efc592f6dc': '08: デバッグエージェント',
    '6862397f1428c1efc592f6de': '09: デプロイスペシャリスト',
    '6862397f1428c1efc592f6e0': '10: 拡張オーケストレーター',
    '6862397f1428c1efc592f6e2': '11: 新ページ作成エージェント',
    '6862397f1428c1efc592f6e4': '12: リファクタリング計画エージェント',
    '6862397f1428c1efc592f6e6': '13: リファクタリング実装エージェント',
}

# プロンプトIDからエージェント名への逆引きマップ
ID_TO_AGENT = {v: k for k, v in PROMPT_MAPPING.items()}

def get_prompt_id(agent_name: str) -> str | None:
    """エージェント名からPortal プロンプトIDを取得"""
    return PROMPT_MAPPING.get(agent_name)

def get_prompt_id_by_agent_name(agent_name: str) -> int:
    """エージェント名から数値プロンプトIDを取得（テスト用）"""
    agent_names = list(PROMPT_MAPPING.keys())
    if agent_name in agent_names:
        return agent_names.index(agent_name)
    raise ValueError(f"Unknown agent name: {agent_name}")

def get_agent_name(prompt_id: str) -> str | None:
    """Portal プロンプトIDからエージェント名を取得"""
    return ID_TO_AGENT.get(prompt_id)

def get_prompt_title(prompt_id: str) -> str:
    """Portal プロンプトIDからタイトルを取得"""
    return PROMPT_TITLES.get(prompt_id, 'Unknown Prompt')

def is_portal_prompt(agent_name: str) -> bool:
    """エージェント名がPortal連携対象かチェック"""
    return agent_name in PROMPT_MAPPING

def get_all_agents() -> list[str]:
    """全エージェント名のリストを取得"""
    return list(PROMPT_MAPPING.keys())

def get_all_prompt_ids() -> list[str]:
    """全プロンプトIDのリストを取得"""
    return list(PROMPT_MAPPING.values())

