from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS, LEAD_TIME_DAYS, SAFETY_BUFFER_DAYS
import math

class InventoryIntelligenceAgent(BaseAgent):
    """
    Priority 1: Critical - Predictive agent that identifies stockout risks 
    and calculates optimal reorder quantities.
    """
    def __init__(self):
        super().__init__("InventoryIntelligenceAgent", "analysis", 1)

    def evaluate(self, context):
        row = context.inventory_data
        kb_ctx = context.domain_knowledge
        
        # Trigger if predicted stockout is within the buffer window
        if row['Days_Until_Stockout'] < REORDER_BUFFER_DAYS:
            # Domain Knowledge Injection
            priority = self.priority
            criticality_note = ""
            
            if kb_ctx.get('criticality') == 'Critical':
                priority = 1 # Force Critical priority for life-saving meds
                criticality_note = " [CRITICAL MEDICINE]"
            
            # Optimal Reorder Quantity Calculation
            # Formula: Avg Daily Usage * (Lead Time + Safety Buffer)
            daily_usage = row.get('Avg_Daily_Usage', 0)
            suggested_qty = daily_usage * (LEAD_TIME_DAYS + SAFETY_BUFFER_DAYS)
            
            # Practical rounding: Always round up to nearest whole unit
            suggested_qty = max(0, math.ceil(suggested_qty))
            
            alert = {
                "type": "SMART_REORDER",
                "priority": priority,
                "message": f"Predicted stockout in {row['Days_Until_Stockout']} days.{criticality_note} Recommended reorder: {suggested_qty} units.",
                "reorder_qty": suggested_qty
            }
            context.risk_flags["SMART_REORDER"] = alert
            return alert
        return None
