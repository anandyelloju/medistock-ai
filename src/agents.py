def reorder_agent(row):
    if row['Stock_Quantity'] < row['Min_Stock_Level']:
        return "REORDER"
    return None

def expiry_agent(row):
    if row['Days_To_Expiry'] < 60:
        return "EXPIRY_RISK"
    return None

def dead_stock_agent(row):
    if row['Days_Since_Last_Sale'] > 180:
        return "DEAD_STOCK"
    return None