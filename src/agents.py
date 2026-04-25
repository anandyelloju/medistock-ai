from .config import EXPIRY_THRESHOLD_DAYS, DEAD_STOCK_DAYS, REORDER_BUFFER_DAYS

def reorder_agent(row):
    """Priority 2: Warning"""
    # Incorporates a buffer from config (defaults to 0 for unchanged behavior)
    if row['Stock_Quantity'] < (row['Min_Stock_Level'] + REORDER_BUFFER_DAYS):
        return ("REORDER", 2)
    return (None, None)

def expiry_agent(row):
    """Priority 1: Critical"""
    if row['Days_To_Expiry'] < EXPIRY_THRESHOLD_DAYS:
        return ("EXPIRY", 1)
    return (None, None)

def dead_stock_agent(row):
    """Priority 3: Info"""
    if row['Days_Since_Last_Sale'] > DEAD_STOCK_DAYS:
        return ("DEAD_STOCK", 3)
    return (None, None)