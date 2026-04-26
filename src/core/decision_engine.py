from ..agents import ReorderAgent, ExpiryAgent, DeadStockAgent, InventoryIntelligenceAgent, ReorderExecutionAgent

# Initialize agents for chaining
expiry_agent = ExpiryAgent()
dead_stock_agent = DeadStockAgent()
intel_agent = InventoryIntelligenceAgent()
exec_agent = ReorderExecutionAgent()
basic_reorder = ReorderAgent()

def evaluate_row(row):
    """
    Evaluates an inventory item using a multi-agent chaining pipeline.
    The chain flows from Risk Detection -> Action Planning.
    """
    alerts = {}

    # 1. Independent Risk Checks
    res_expiry = expiry_agent.evaluate(row)
    if res_expiry: alerts['EXPIRY'] = res_expiry

    res_dead = dead_stock_agent.evaluate(row)
    if res_dead: alerts['DEAD_STOCK'] = res_dead

    # 2. Chained Reorder Logic (Intelligence -> Execution)
    # Phase A: Risk Detection
    risk_alert = intel_agent.evaluate(row)
    
    if risk_alert:
        alerts['SMART_REORDER'] = risk_alert
        
        # Phase B: Action Planning (Only runs if risk is detected)
        plan_alert = exec_agent.evaluate(row)
        if plan_alert:
            alerts['EXECUTION_PLAN'] = plan_alert
    else:
        # Phase C: Fallback to Basic Reorder
        # Only checked if the predictive intelligence didn't trigger
        basic_alert = basic_reorder.evaluate(row)
        if basic_alert:
            alerts['REORDER'] = basic_alert

    return list(alerts.values())