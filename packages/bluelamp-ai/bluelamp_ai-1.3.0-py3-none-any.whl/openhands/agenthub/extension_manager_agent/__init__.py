from openhands.agenthub.extension_manager_agent.extension_manager_agent import ExtensionManagerAgent
from openhands.controller.agent import Agent

# ExtensionManagerAgentとして登録
Agent.register('ExtensionManagerAgent', ExtensionManagerAgent)
