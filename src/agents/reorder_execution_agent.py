from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS, LEAD_TIME_DAYS, SAFETY_BUFFER_DAYS
import math

class ReorderExecutionAgent(BaseAgent):
    """
    Priority 2: Warning - Defines the technical execution plan for inventory replenishment.
    Calculates optimal order quantities and determines procurement urgency based on lead times.
    """
    def __init__(self):
        super().__init__("ReorderExecutionAgent", "decision", 2, dependencies=["InventoryIntelligenceAgent"])

    def evaluate(self, context):
        row = context.inventory_data
        kb_ctx = context.domain_knowledge

        # Only triggers if a stockout risk is detected (within buffer window)
        if row['Days_Until_Stockout'] < REORDER_BUFFER_DAYS:
            daily_usage = row.get('Avg_Daily_Usage', 0)
            seasonal_multiplier = 1.0
            seasonal_note = ""

            # Domain Knowledge Injection: Seasonality
            if "High" in kb_ctx.get('seasonal_info', ''):
                seasonal_multiplier = 1.5 # Increase stock for peak seasons
                seasonal_note = f" (Adjusted for {kb_ctx['seasonal_info']} demand)"

            # 1. Calculate Reorder Quantity
            plan_qty = math.ceil(daily_usage * (LEAD_TIME_DAYS + SAFETY_BUFFER_DAYS) * seasonal_multiplier)
            
            # 2. Determine Urgency Level
            if row['Days_Until_Stockout'] < LEAD_TIME_DAYS:
                urgency = "CRITICAL (Stockout expected before delivery)"
            elif row['Days_Until_Stockout'] < (LEAD_TIME_DAYS + (SAFETY_BUFFER_DAYS / 2)):
                urgency = "HIGH (Low safety margin)"
            else:
                urgency = "NORMAL"

            alert = {
                "type": "EXECUTION_PLAN",
                "priority": self.priority,
                "message": f"Plan: Reorder {plan_qty} units {seasonal_note}. Urgency: {urgency}.",
                "reorder_qty": plan_qty,
                "urgency": urgency
            }
            context.decisions["EXECUTION_PLAN"] = alert
            return alert
            
        return None
