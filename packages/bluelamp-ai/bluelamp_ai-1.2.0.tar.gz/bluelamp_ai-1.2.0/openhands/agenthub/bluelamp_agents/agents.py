"""BlueLamp専門エージェント群"""

import os
from typing import List, Dict, Any, Optional
from openhands.agenthub.orchestrator_agent.orchestrator_agent import OrchestratorAgent
from openhands.controller.state.state import State
from openhands.events.action import AgentFinishAction
from openhands.utils.prompt import PromptManager
from openhands.portal.portal_prompt_manager import PortalPromptManager
from openhands.core.logger import openhands_logger as logger


class BlueLampBaseAgent(OrchestratorAgent):
    """BlueLamp専門エージェントの基底クラス"""

    VERSION = '1.0'

    @property
    def prompt_manager(self) -> PromptManager:
        """BlueLampエージェント用のPortalプロンプトマネージャーを返す"""
        if self._prompt_manager is None:
            # BlueLampエージェントのプロンプトディレクトリを使用（フォールバック用）
            prompt_dir = os.path.join(os.path.dirname(__file__), 'prompts')
            
            
            # PortalPromptManagerを使用（Portal優先、ローカルフォールバック）
            self._prompt_manager = PortalPromptManager(
                prompt_dir=prompt_dir,
                system_prompt_filename=self.config.system_prompt_filename,
                enable_portal=True  # Portal連携を有効化
            )
            
            logger.info(f"PortalPromptManager initialized for {self.config.system_prompt_filename}")
        return self._prompt_manager

    def _get_tools(self) -> List[Any]:
        """委譲ツールを除外したツールリストを返す"""
        tools = super()._get_tools()
        # 委譲関連ツールを除外（delegate_で始まるツール名）
        filtered_tools = []
        for tool in tools:
            # ChatCompletionToolParamオブジェクトの場合
            if hasattr(tool, 'function') and hasattr(tool.function, 'name'):  # type: ignore
                if not tool.function.name.startswith('delegate_'):  # type: ignore
                    filtered_tools.append(tool)
            # dict形式の場合
            elif isinstance(tool, dict) and 'function' in tool:
                if not tool.get('function', {}).get('name', '').startswith('delegate_'):
                    filtered_tools.append(tool)
            else:
                # その他のツールはそのまま含める
                filtered_tools.append(tool)
        return filtered_tools


# 16個の専門エージェント定義
class RequirementsEngineer(BlueLampBaseAgent):
    """★1 要件定義エンジニア: プロジェクトの要件定義書を作成"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'requirements_engineer'
        super().__init__(llm, config)


class UIUXDesigner(BlueLampBaseAgent):
    """★2 UI/UXデザイナー: ユーザーインターフェースとエクスペリエンスを設計"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'uiux_designer'
        super().__init__(llm, config)


class DataModelingEngineer(BlueLampBaseAgent):
    """★3 データモデリングエンジニア: データベース設計とER図作成"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'data_modeling_engineer'
        super().__init__(llm, config)


class SystemArchitect(BlueLampBaseAgent):
    """★4 システムアーキテクト: システム全体のアーキテクチャ設計"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'system_architect'
        super().__init__(llm, config)


class ImplementationConsultant(BlueLampBaseAgent):
    """★5 実装計画コンサルタント: 実装戦略と技術選定"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'implementation_consultant'
        super().__init__(llm, config)


class EnvironmentSetup(BlueLampBaseAgent):
    """★6 環境構築: 開発環境とインフラ構築"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'environment_setup'
        super().__init__(llm, config)


class PrcImplementation(BlueLampBaseAgent):
    """★7 PRC実装: プロトタイプ実装とコア機能開発"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'prc_implementation'
        super().__init__(llm, config)


class DebugAgent(BlueLampBaseAgent):
    """★8 デバッグエージェント: バグ修正とエラー解決"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'debug_agent'
        super().__init__(llm, config)


class DeploySpecialist(BlueLampBaseAgent):
    """★9 デプロイ専門家: デプロイメントとインフラ管理"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'deploy_specialist'
        super().__init__(llm, config)


class ExpansionOrchestrator(BlueLampBaseAgent):
    """★10 拡張オーケストレーター: 機能拡張の統合管理"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'expansion_orchestrator'
        super().__init__(llm, config)


class PageCreator(BlueLampBaseAgent):
    """★11 ページ作成: 新規ページとコンポーネント作成"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'page_creator'
        super().__init__(llm, config)


class RefactoringEngineer(BlueLampBaseAgent):
    """★12 リファクタリングエンジニア: コード改善計画策定と実装"""
    def __init__(self, llm: Any, config: Any = None):
        if config is None:
            from openhands.core.config import AgentConfig
            config = AgentConfig()
        config.system_prompt_filename = 'refactoring_engineer'
        super().__init__(llm, config)


