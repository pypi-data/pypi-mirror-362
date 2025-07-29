from openhands.agenthub.orchestrator_agent.orchestrator_agent import OrchestratorAgent
from openhands.controller.agent import Agent

# OrchestratorAgentとして登録
Agent.register('OrchestratorAgent', OrchestratorAgent)
