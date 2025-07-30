"""BlueLamp Delegate Tools"""

from litellm import ChatCompletionToolParam

# BlueLamp専門エージェント委譲ツール定義

def create_bluelamp_delegate_tools():
    """12個のBlueLamp専門エージェントへの委譲ツールを生成（Portal APIマッピング準拠）"""
    return [
        # ★1 要件定義エンジニア
        ChatCompletionToolParam(
            type='function',
            function={
                'name': 'delegate_to_requirements_engineer',
                'description': '要件定義タスクをRequirementsEngineerに委譲。新規プロジェクトの要件定義書作成、既存要件のブラッシュアップ、曖昧な仕様の具体化を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'ユーザーのヒアリングをして要件定義書を作成しSCOPE_PROGRESSを更新'},
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
                'description': 'UI/UXデザインタスクをUIUXDesignerに委譲。要件定義からモックアップ作成、デザインシステム構築、データ契約基盤作成を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '要件定義書に記載された全ページのモックアップ、データ契約基盤を構築し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': 'データモデル設計タスクをDataModelingEngineerに委譲。要件定義とモックアップからデータ契約最適化、ディレクトリ構造設計、整合性検証を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '要件定義とモックアップからデータ契約を最適化し、ディレクトリ構造を設計し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': 'システムアーキテクチャ設計タスクをSystemArchitectに委譲。ユーザーロール明確化、認証方針決定、基本認証方針書作成を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'ユーザーにヒアリングして認証システムを設計し基本認証方針書を作成し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': '実装計画策定タスクをImplementationConsultantに委譲。全ページのPRC作成、実装順序決定、SCOPE_PROGRESS更新を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '要件定義書に記載された全ページのPRC作成と実装順序決定を行い、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': '開発環境構築タスクをEnvironmentSetupに委譲。外部サービス設定、環境変数構築、Git初期設定を非技術者向けにガイドして代行する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'ユーザーを丁寧にガイドして外部サービス設定と環境変数構築を代行し、Git初期設定を完了し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': 'PRC実装タスクをPrcImplementationに委譲。Backend実装、統合テスト、Frontend UI、API統合を段階的に実装し、実データ主義で品質保証する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '指定されたPRCを6段階のPhaseで段階的に実装し、実データ主義で品質保証を行い、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': 'デバッグタスクをDebugAgentに委譲。エラー分類、根本原因特定、クリーンコードスコア向上修正、型整合性確保を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'エラーを分類して根本原因を特定し、クリーンコードスコアを向上させる修正で解決し、ユーザーからの要望を全て満たし完了許可をユーザーから取得する'},
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
                'description': 'デプロイタスクをDeploySpecialistに委譲。非技術者向けガイドで本番環境構築、CI/CDパイプライン設定、既存サービス保護を代行する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': '非技術者を丁寧にガイドして本番環境デプロイとCI/CDパイプライン構築を代行し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': '新ページ作成タスクをPageCreatorに委譲。要件ヒアリング、モックアップ作成、API仕様定義、PRC作成まで一貫して新ページ追加を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'ユーザーにヒアリングして新ページの要件を確定し、モックアップ作成、API仕様定義、PRC作成まで一貫して実行し、エージェントプロンプトに内包されている完了基準を全て満たす'},
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
                'description': 'リファクタリングタスクをRefactoringEngineerに委譲。不要コードのローラー作戦による徹底除去、連鎖削除、システム軽量化を依頼する際に使用',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task': {'type': 'string', 'description': 'プロジェクト内の不要コードをローラー作戦で徹底除去し、連鎖削除によるシステム軽量化を行い、エージェントプロンプトに内包されている完了基準を全て満たす'},
                    },
                    'required': ['task']
                }
            }
        ),
    ]
