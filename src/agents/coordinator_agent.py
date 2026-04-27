from .base_agent import BaseAgent, SharedContext

class CoordinatorAgent:
    """
    The Orchestrator of the MediStock AI system.
    Responsible for managing the execution flow of all specialized agents
    using a SharedContext for communication.
    """
    def __init__(self, agents):
        self.agents = agents
        self.analysis_agents = [a for a in agents if a.role == 'analysis']
        self.decision_agents = [a for a in agents if a.role == 'decision']
        self.execution_agents = [a for a in agents if a.role == 'execution']

    def orchestrate(self, row, domain_knowledge=None):
        """
        Executes a dynamic, dependency-aware workflow using SharedContext.
        """
        # Initialize Shared Context
        ctx = SharedContext(inventory_data=row, domain_knowledge=domain_knowledge)
        executed_agent_names = set()

        # 1. PHASE 1: ANALYSIS
        for agent in self.analysis_agents:
            agent.evaluate(ctx)
            executed_agent_names.add(agent.name)

        # 2. PHASE 2: DECISION
        for agent in self.decision_agents:
            can_run = not agent.dependencies or any(dep in executed_agent_names for dep in agent.dependencies)
            if can_run:
                agent.evaluate(ctx)
                executed_agent_names.add(agent.name)

        # 3. PHASE 3: EXECUTION
        for agent in self.execution_agents:
            can_run = any(dep in executed_agent_names for dep in agent.dependencies)
            if can_run:
                agent.evaluate(ctx)
                executed_agent_names.add(agent.name)

        return ctx.get_all_alerts()
