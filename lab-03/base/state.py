from abc import ABC, abstractmethod
from abc import ABC


class State(ABC):

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
