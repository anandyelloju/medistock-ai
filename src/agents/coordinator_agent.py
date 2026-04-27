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
        Executes a controlled workflow for a single inventory item.
        """
        alerts = {}

        # 1. PHASE 1: ANALYSIS (Risk Detection)
        # Always run these to gather the current state of risk
        for agent in self.analysis_agents:
            res = agent.evaluate(row, context=context)
            if res:
                alerts[res['type']] = res

        # 2. PHASE 2: DECISION (Planning)
        # Only trigger if an analysis agent detected a reorder risk
        # This prevents redundant planning for healthy inventory
        has_reorder_risk = any(t in alerts for t in ['SMART_REORDER', 'REORDER'])
        
        if has_reorder_risk:
            for agent in self.decision_agents:
                res = agent.evaluate(row, context=context)
                if res:
                    # In decision phase, new context might be added (e.g., quantities)
                    alerts[res['type']] = res

        # 3. PHASE 3: EXECUTION (Action)
        # Only trigger if a formal plan was created in the decision phase
        if 'EXECUTION_PLAN' in alerts:
            plan = alerts['EXECUTION_PLAN']
            for agent in self.execution_agents:
                # Execution agents often require the 'plan' from the previous phase
                # We handle this by passing it as a keyword argument
                try:
                    res = agent.evaluate(row, context=context, plan=plan)
                except TypeError:
                    # Fallback for agents that don't support the 'plan' argument yet
                    res = agent.evaluate(row, context=context)
                
                if res:
                    alerts[res['type']] = res

        return list(alerts.values())
