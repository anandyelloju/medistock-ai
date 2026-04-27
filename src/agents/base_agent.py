from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Base class for all inventory agents.
    Provides a standard structure for evaluation and priority handling.
    """
    def __init__(self, name, role, priority, dependencies=None):
        self.name = name
        self.role = role
        self.priority = priority
        self.dependencies = dependencies or []

    @abstractmethod
    def evaluate(self, row, context=None):
        """Processes a row of data with optional context and returns an alert dict or None."""
        pass
