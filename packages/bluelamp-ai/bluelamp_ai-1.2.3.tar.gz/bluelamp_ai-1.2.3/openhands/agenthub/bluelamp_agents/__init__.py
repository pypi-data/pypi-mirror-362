"""
BlueLamp専門エージェント群

12個のBlueLampエージェントが13エージェント構造（00-12）にマッピング:
- 00: orchestrator (OrchestratorAgent用)
- 01-12: 各BlueLampエージェントが対応
- RefactoringPlannerとRefactoringImplementationを統合してRefactoringEngineerに
- Portal API統合完了
"""

from .agents import (
    RequirementsEngineer,
    UIUXDesigner,
    DataModelingEngineer,
    SystemArchitect,
    ImplementationConsultant,
    EnvironmentSetup,
    PrcImplementation,
    DebugAgent,
    DeploySpecialist,
    ExpansionOrchestrator,
    PageCreator,
    RefactoringEngineer,
)
from openhands.controller.agent import Agent

# 12個のBlueLampエージェント - クラス名とプロンプトが一致
BLUELAMP_AGENTS = [
    ('RequirementsEngineer', RequirementsEngineer),
    ('UIUXDesigner', UIUXDesigner),
    ('DataModelingEngineer', DataModelingEngineer),
    ('SystemArchitect', SystemArchitect),
    ('ImplementationConsultant', ImplementationConsultant),
    ('EnvironmentSetup', EnvironmentSetup),
    ('PrcImplementation', PrcImplementation),
    ('DebugAgent', DebugAgent),
    ('DeploySpecialist', DeploySpecialist),
    ('ExpansionOrchestrator', ExpansionOrchestrator),
    ('PageCreator', PageCreator),
    ('RefactoringEngineer', RefactoringEngineer),
]

for name, cls in BLUELAMP_AGENTS:
    Agent.register(name, cls)

__all__ = [name for name, _ in BLUELAMP_AGENTS]
