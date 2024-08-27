import numpy as np
from abc import ABC, abstractmethod
from game.game import Action


class Agent(ABC):
    @abstractmethod
    def act(self, observation: np.ndarray) -> Action:
        """
        Act given an observation

        :param observation: Observation numpy array
        """

        raise NotImplementedError()
