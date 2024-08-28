from enum import Enum
from agent.agent import Agent
from agent.random_agent import RandomAgent


class AgentType(Enum):
    """
    Enum for agent types
    """

    RANDOM = 0


def get_agent(self, agent_type: AgentType) -> Agent:
    """
    Get an agent instance given an agent type
    """

    match agent_type:
        case AgentType.RANDOM:
            return RandomAgent()
        case _:
            raise ValueError(f"Unsupported agent type: {agent_type}")

