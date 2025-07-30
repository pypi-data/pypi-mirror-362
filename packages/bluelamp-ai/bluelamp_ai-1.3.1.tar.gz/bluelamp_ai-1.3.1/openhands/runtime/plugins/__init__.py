# Requirements
from openhands.runtime.plugins.agent_skills import (
    AgentSkillsPlugin,
    AgentSkillsRequirement,
)
from openhands.runtime.plugins.requirement import Plugin, PluginRequirement
from openhands.runtime.plugins.vscode import VSCodePlugin, VSCodeRequirement

__all__ = [
    'Plugin',
    'PluginRequirement',
    'AgentSkillsRequirement',
    'AgentSkillsPlugin',
    'VSCodeRequirement',
    'VSCodePlugin',
]

ALL_PLUGINS = {
    'agent_skills': AgentSkillsPlugin,
    'vscode': VSCodePlugin,
}
