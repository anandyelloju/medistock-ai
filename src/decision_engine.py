from .agents import ReorderAgent, ExpiryAgent, DeadStockAgent

# Initialize the agent suite
inventory_agents = [
    ReorderAgent(),
    ExpiryAgent(),
    DeadStockAgent()
]

def evaluate_row(row):
    """
    Evaluates an inventory item using a suite of automated agents.
    Iterates through all registered agents and collects their findings.
    """
    alerts = []

    for agent in inventory_agents:
        alert = agent.evaluate(row)
        if alert:
            alerts.append(alert)

    return alerts