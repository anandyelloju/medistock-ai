from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS, LEAD_TIME_DAYS, SAFETY_BUFFER_DAYS
import math

class InventoryIntelligenceAgent(BaseAgent):
    """
    Priority 1: Critical - Predictive agent that identifies stockout risks 
    and calculates optimal reorder quantities.
    """
    def __init__(self):
        super().__init__("InventoryIntelligenceAgent", 1)

    def evaluate(self, row):
        # Trigger if predicted stockout is within the buffer window
        if row['Days_Until_Stockout'] < REORDER_BUFFER_DAYS:
            # Optimal Reorder Quantity Calculation
            # Formula: Avg Daily Usage * (Lead Time + Safety Buffer)
            daily_usage = row.get('Avg_Daily_Usage', 0)
            suggested_qty = daily_usage * (LEAD_TIME_DAYS + SAFETY_BUFFER_DAYS)
            
            # Practical rounding: Always round up to nearest whole unit
            suggested_qty = max(0, math.ceil(suggested_qty))
            
            return {
                "type": "SMART_REORDER",
                "priority": self.priority,
                "message": f"Predicted stockout in {row['Days_Until_Stockout']} days. Recommended reorder: {suggested_qty} units.",
                "reorder_qty": suggested_qty
            }
        return None
