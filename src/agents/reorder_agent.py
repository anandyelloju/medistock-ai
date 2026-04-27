from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS

class ReorderAgent(BaseAgent):
    """Priority 2: Warning - Detects low stock levels."""
    def __init__(self):
        super().__init__("ReorderAgent", "decision", 2)

    def evaluate(self, context):
        row = context.inventory_data
        if row['Stock_Quantity'] < (row['Min_Stock_Level'] + REORDER_BUFFER_DAYS):
            alert = {
                "type": "REORDER",
                "priority": self.priority,
                "message": "Stock below minimum level."
            }
            context.decisions["REORDER"] = alert
            return alert
        return None
