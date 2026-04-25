from .base_agent import BaseAgent
from ..config import REORDER_BUFFER_DAYS

class ReorderAgent(BaseAgent):
    """Priority 2: Warning - Detects low stock levels."""
    def __init__(self):
        super().__init__("ReorderAgent", 2)

    def evaluate(self, row):
        if row['Stock_Quantity'] < (row['Min_Stock_Level'] + REORDER_BUFFER_DAYS):
            return {
                "type": "REORDER",
                "priority": self.priority,
                "message": "Stock below minimum level."
            }
        return None
