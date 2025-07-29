"""BlueLamp Delegate Tools"""

from litellm import ChatCompletionToolParam

# BlueLamp専門エージェント委譲ツール定義

def create_bluelamp_delegate_tools():
    """16個のBlueLamp専門エージェントへの委譲ツールを生成"""
    return [
        # ★1 要件定義エンジニア
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_requirements_engineer',
                'description': '要件定義タスクをRequirementsEngineerに委譲。新規プロジェクトの要件定義書作成を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行する要件定義タスクの詳細'},
                        'context': {'type': 'object', 'description': 'プロジェクト情報などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★2 UI/UXデザイナー
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_ui_ux_designer',
                'description': 'UI/UXデザインタスクをUIUXDesignerに委譲。モックアップやデザイン作成を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するUI/UXデザインタスクの詳細'},
                        'context': {'type': 'object', 'description': 'デザイン要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★3 データモデリングエンジニア
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_data_modeling_engineer',
                'description': 'データモデル設計タスクをDataModelingEngineerに委譲。型定義やAPI設計を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するデータモデリングタスクの詳細'},
                        'context': {'type': 'object', 'description': 'データ要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★4 システムアーキテクト
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_system_architect',
                'description': 'システムアーキテクチャ設計タスクをSystemArchitectに委譲。認証・権限設計を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するシステム設計タスクの詳細'},
                        'context': {'type': 'object', 'description': 'システム要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★5 実装計画コンサルタント
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_implementation_consultant',
                'description': '実装計画策定タスクをImplementationConsultantに委譲。実装戦略と技術選定を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行する実装計画タスクの詳細'},
                        'context': {'type': 'object', 'description': 'プロジェクト要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★6 環境構築
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_environment_setup',
                'description': '開発環境構築タスクをEnvironmentSetupに委譲。初期設定やインフラ構築を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行する環境構築タスクの詳細'},
                        'context': {'type': 'object', 'description': '環境要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★7 PRC実装
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_prc_implementation',
                'description': 'PRC実装タスクをPrcImplementationに委譲。プロトタイプ実装とコア機能開発を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するPRC実装タスクの詳細'},
                        'context': {'type': 'object', 'description': '実装要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★08 デバッグエージェント
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_debug_agent',
                'description': 'デバッグタスクをDebugAgentに委譲。エラー調査と修正を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するデバッグタスクの詳細'},
                        'error': {'type': 'string', 'description': 'エラーメッセージやスタックトレース'},
                        'context': {'type': 'object', 'description': 'デバッグに必要な追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★11 新ページ作成エージェント
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_page_creator',
                'description': '新ページ作成タスクをPageCreatorに委譲。新しいページの作成と実装を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するページ作成タスクの詳細'},
                        'context': {'type': 'object', 'description': 'ページ作成要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★09 デプロイスペシャリスト
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_deploy_specialist',
                'description': 'デプロイタスクをDeploySpecialistに委譲。本番環境構築とデプロイを依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するデプロイタスクの詳細'},
                        'context': {'type': 'object', 'description': 'デプロイ要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),

        # ★12 リファクタリングエンジニア
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_refactoring_engineer',
                'description': 'リファクタリングタスクをRefactoringEngineerに委譲。コード分析、計画策定、実装まで統合的に依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '実行するリファクタリングタスクの詳細'},
                        'context': {'type': 'object', 'description': 'コード改善要件などの追加コンテキスト'},
                        'requirements': {'type': 'string', 'description': '制約条件・要件'},
                    },
                    'required': ['task']
                }
            }
        ),
    ]
