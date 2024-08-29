from enum import Enum
from agent.agent import Agent
from agent.random_agent import RandomAgent
from agent.biased_random_agent import BiasedRandomAgent


class AgentType(Enum):
    """
    Enum for agent types
    """

    RANDOM = 0
    BIASED_RANDOM = 1


def get_agent(agent_type: AgentType) -> Agent:
    """
    Get an agent instance given an agent type
    """

    match agent_type:
        case AgentType.RANDOM:
            return RandomAgent()
        case AgentType.BIASED_RANDOM:
            return BiasedRandomAgent()
        case _:
            raise ValueError(f"Unsupported agent type: {agent_type}")

