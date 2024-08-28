import random
import numpy as np
from agent.agent import Agent
from game.action import Action


class RandomAgent(Agent):
    """
    Act by selecting a random action with equal probability.
    """

    ACTIONS = list(Action)

    def get_action(self, observation: np.ndarray) -> Action: 
        return random.choice(self.ACTIONS)
