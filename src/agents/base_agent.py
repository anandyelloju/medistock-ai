from abc import ABC, abstractmethod

class SharedContext:
    """
    A unified communication object passed between agents during orchestration.
    Enables decoupled data exchange between Analysis, Decision, and Execution layers.
    """
    def __init__(self, inventory_data, domain_knowledge=None):
        self.inventory_data = inventory_data
        self.domain_knowledge = domain_knowledge or {}
        self.risk_flags = {}  # Written by 'analysis' agents
        self.decisions = {}   # Written by 'decision' agents
        self.actions = {}     # Written by 'execution' agents

    def get_all_alerts(self):
        """Returns a unified list of all results stored in the context."""
        all_alerts = {**self.risk_flags, **self.decisions, **self.actions}
        return list(all_alerts.values())

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
    def evaluate(self, context: SharedContext):
        """
        Evaluates the current context and performs role-specific logic.
        Agents should read from context.inventory_data and write to 
        risk_flags, decisions, or actions depending on their role.
        """
        pass
