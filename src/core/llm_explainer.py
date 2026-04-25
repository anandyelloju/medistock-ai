def generate_explanation(row, alerts):
    """
    Generates a structured, actionable explanation for inventory alerts.
    Format: [Problem] -> [Business Impact] -> [Recommended Action]
    """
    explanations = []

    for alert in alerts:
        if alert['type'] == 'REORDER':
            impact = "Risk of stockout, leading to lost revenue and patient care delays."
            action = f"Order fresh stock from {row['Supplier_Name']} immediately."
        elif alert['type'] == 'EXPIRY':
            impact = "Financial loss due to expired inventory that cannot be sold."
            action = "Run a 'First-to-Expire' sales promotion or check return policy."
        elif alert['type'] == 'DEAD_STOCK':
            impact = "Capital tied up in non-moving stock, reducing liquidity."
            action = "Offer discounts or bundle with fast-moving items to liquidate."
        else:
            continue

        explanations.append(
            f"**{alert['type']} ALERT**\n"
            f"🚩 **Problem**: {alert['message']}\n"
            f"📉 **Business Impact**: {impact}\n"
            f"✅ **Recommended Action**: {action}"
        )

    return "\n\n".join(explanations)