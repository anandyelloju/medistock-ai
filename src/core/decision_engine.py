from ..agents import ReorderAgent, ExpiryAgent, DeadStockAgent, InventoryIntelligenceAgent

# Initialize the agent suite
inventory_agents = [
    ReorderAgent(),
    ExpiryAgent(),
    DeadStockAgent(),
    InventoryIntelligenceAgent()
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

    # Override Logic: Smart reorder provides better context than basic reorder
    if "SMART_REORDER" in raw_alerts and "REORDER" in raw_alerts:
        # Keep the smart one as it has higher priority and better reasoning
        del raw_alerts["REORDER"]

    return list(raw_alerts.values())