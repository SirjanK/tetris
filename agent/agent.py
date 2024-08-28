import numpy as np
from abc import ABC, abstractmethod
from game.game import Action


class Agent(ABC):
    @abstractmethod
    def get_action(self, observation: np.ndarray) -> Action:
        """
        Get an action given the observation

        :param observation: Observation numpy array
        """

        raise NotImplementedError()
