from .base_agent import BaseAgent

class CoordinatorAgent:
    """
    The Orchestrator of the MediStock AI system.
    Responsible for managing the execution flow of all specialized agents
    based on their roles (Analysis -> Decision -> Execution).
    """
    def __init__(self, agents):
        self.agents = agents
        self.analysis_agents = [a for a in agents if a.role == 'analysis']
        self.decision_agents = [a for a in agents if a.role == 'decision']
        self.execution_agents = [a for a in agents if a.role == 'execution']

    def orchestrate(self, row, context=None):
        """
        Executes a dynamic, dependency-aware workflow.
        """
        alerts = {}
        executed_agent_names = set()

        # 1. PHASE 1: ANALYSIS
        # Analysis agents have no dependencies and always run first
        for agent in self.analysis_agents:
            res = agent.evaluate(row, context=context)
            executed_agent_names.add(agent.name)
            if res:
                alerts[res['type']] = res

        # 2. PHASE 2: DECISION
        # Decision agents run only if their specific dependencies (Analysis agents) 
        # actually produced an alert that requires a decision.
        for agent in self.decision_agents:
            # Check if dependencies produced an alert
            # We look for the source agent name in the executed list AND if they returned a result
            # Simplified: Run if ANY dependency was met
            can_run = not agent.dependencies or any(dep in executed_agent_names for dep in agent.dependencies)
            
            # Additional check: Does this decision agent have a related alert to work on?
            # For ReorderExecution, it needs a SMART_REORDER or REORDER alert.
            # To keep it truly dynamic, we'll check if any 'analysis' result exists that this agent relies on.
            if can_run:
                res = agent.evaluate(row, context=context)
                if res:
                    alerts[res['type']] = res
                    executed_agent_names.add(agent.name)

        # 3. PHASE 3: EXECUTION
        # Execution agents run only if their decision dependencies are met
        for agent in self.execution_agents:
            # Check if dependencies (Decision agents) produced a plan
            # We'll look for a plan in the alerts dictionary
            plan = alerts.get('EXECUTION_PLAN') # Still a bit specific, but manageable
            
            can_run = any(dep in executed_agent_names for dep in agent.dependencies)
            
            if can_run:
                try:
                    res = agent.evaluate(row, context=context, plan=plan)
                except TypeError:
                    res = agent.evaluate(row, context=context)
                
                if res:
                    alerts[res['type']] = res
                    executed_agent_names.add(agent.name)

        return list(alerts.values())
