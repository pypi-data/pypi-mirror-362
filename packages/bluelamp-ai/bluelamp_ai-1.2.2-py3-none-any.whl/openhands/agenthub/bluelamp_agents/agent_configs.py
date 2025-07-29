# エージェント別の固定タスク設定

AGENT_FIXED_TASKS = {
    'RefactoringEngineer': {
        'task': 'プロジェクト全体のコード品質改善とリファクタリング'
    },
    'DebugAgent': {
        'task': 'エラーの調査と修正'
    },
    'PageCreator': {
        'task': '新しいページの作成と実装'
    }
}

def get_fixed_task(agent_name: str, original_task: str = None) -> str:
    """エージェント名に基づいて固定タスクを取得"""
    if agent_name in AGENT_FIXED_TASKS:
        return AGENT_FIXED_TASKS[agent_name]['task']
    return original_task or "タスクを実行してください"

