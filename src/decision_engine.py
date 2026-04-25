from .agents import reorder_agent, expiry_agent, dead_stock_agent

def evaluate_row(row):
    """
    Evaluates an inventory item and returns structured alerts with priority scores.
    """
    alerts = []

    # Reorder Check
    res_type, res_prio = reorder_agent(row)
    if res_type:
        alerts.append({
            "type": res_type,
            "priority": res_prio,
            "message": "Stock below minimum level."
        })

    # Expiry Check
    res_type, res_prio = expiry_agent(row)
    if res_type:
        alerts.append({
            "type": res_type,
            "priority": res_prio,
            "message": "Item is approaching expiry date."
        })

    # Dead Stock Check
    res_type, res_prio = dead_stock_agent(row)
    if res_type:
        alerts.append({
            "type": res_type,
            "priority": res_prio,
            "message": "No recent sales recorded (Dead Stock)."
        })

    return alerts