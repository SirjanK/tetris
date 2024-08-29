import numpy as np
import random
from agent.agent import Agent
from game.action import Action


class BiasedRandomAgent(Agent):
    """
    Act by selecting a random action with biased probabilities.

    Bias towards picking left, right, and rotate actions with lower probability down action. All other actions are picked with low probabilities.
    """

    ACTION_PROBABILITIES = [
        (Action.ROTATE, 0.2),
        (Action.MOVE_LEFT, 0.35),
        (Action.MOVE_RIGHT, 0.35),
        (Action.MOVE_DOWN, 0.01),
        (Action.MOVE_TO_BOTTOM, 0.1),
        (Action.SAVE_BLOCK, 0.01),
    ]
    ACTIONS = [action for action, _ in ACTION_PROBABILITIES]
    PROBABILITIES = np.array([p for _, p in ACTION_PROBABILITIES])

    def get_action(self, observation: np.ndarray) -> Action: 
        return random.choices(self.ACTIONS, weights=self.PROBABILITIES)[0]
