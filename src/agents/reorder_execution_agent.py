from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS, LEAD_TIME_DAYS, SAFETY_BUFFER_DAYS
import math

class ReorderExecutionAgent(BaseAgent):
    """
    Priority 2: Warning - Defines the technical execution plan for inventory replenishment.
    Calculates optimal order quantities and determines procurement urgency based on lead times.
    """
    def __init__(self):
        super().__init__("ReorderExecutionAgent", 2)

    def evaluate(self, row):
        # Only triggers if a stockout risk is detected (within buffer window)
        if row['Days_Until_Stockout'] < REORDER_BUFFER_DAYS:
            daily_usage = row.get('Avg_Daily_Usage', 0)
            
            # 1. Calculate Reorder Quantity
            # Formula: Cover the lead time plus the safety buffer
            plan_qty = math.ceil(daily_usage * (LEAD_TIME_DAYS + SAFETY_BUFFER_DAYS))
            
            # 2. Determine Urgency Level
            if row['Days_Until_Stockout'] < LEAD_TIME_DAYS:
                urgency = "CRITICAL (Stockout expected before delivery)"
            elif row['Days_Until_Stockout'] < (LEAD_TIME_DAYS + (SAFETY_BUFFER_DAYS / 2)):
                urgency = "HIGH (Low safety margin)"
            else:
                urgency = "NORMAL"

            return {
                "type": "EXECUTION_PLAN",
                "priority": self.priority,
                "message": f"Plan: Reorder {plan_qty} units. Urgency: {urgency}.",
                "reorder_qty": plan_qty,
                "urgency": urgency
            }
            
        return None
