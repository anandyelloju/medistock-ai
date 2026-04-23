from .agents import reorder_agent, expiry_agent, dead_stock_agent

def evaluate_row(row):
    decisions = []

    if reorder_agent(row):
        decisions.append("Reorder Required")

    if expiry_agent(row):
        decisions.append("Near Expiry")

    if dead_stock_agent(row):
        decisions.append("No Sales - Risk")

    return decisions