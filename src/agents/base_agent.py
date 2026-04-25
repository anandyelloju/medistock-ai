from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Base class for all inventory agents.
    Provides a standard structure for evaluation and priority handling.
    """
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    @abstractmethod
    def evaluate(self, row):
        """Processes a row of data and returns an alert dict or None."""
        pass
