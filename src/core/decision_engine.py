from ..agents import ReorderAgent, ExpiryAgent, DeadStockAgent, InventoryIntelligenceAgent, ReorderExecutionAgent

# Initialize the agent suite
inventory_agents = [
    ReorderAgent(),
    ExpiryAgent(),
    DeadStockAgent(),
    InventoryIntelligenceAgent(),
    ReorderExecutionAgent()
]

def evaluate_row(row):
    """
    Evaluates an inventory item and merges agent outputs with priority logic.
    Ensures that predictive (SMART) alerts override basic threshold alerts.
    """
    raw_alerts = {}

    for agent in inventory_agents:
        alert = agent.evaluate(row)
        if alert:
            raw_alerts[alert['type']] = alert

    # Override Logic: Smart reorder and execution plans provide better context than basic reorder
    if "REORDER" in raw_alerts:
        if "SMART_REORDER" in raw_alerts or "EXECUTION_PLAN" in raw_alerts:
            # Keep the advanced ones as they have higher priority and better reasoning
            del raw_alerts["REORDER"]

    return list(raw_alerts.values())