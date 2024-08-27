import random
import numpy as np
from agent.agent import Agent
from game.game import Action


class RandomAgent(Agent):
    """
    Act by selecting a random action with equal probability.
    """

    ACTIONS = list(Action)

    def act(self, observation: np.ndarray) -> Action: 
        return random.choice(self.ACTIONS)
