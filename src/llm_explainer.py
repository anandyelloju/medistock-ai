def generate_explanation(row, decisions):
    explanation = f"{row['Item_Name']}: "

    if "Reorder Required" in decisions:
        explanation += "Stock is below minimum level. "

    if "Near Expiry" in decisions:
        explanation += "Item is close to expiry. "

    if "No Sales - Risk" in decisions:
        explanation += "Item has not been sold recently. "

    return explanation