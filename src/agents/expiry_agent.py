from .base_agent import BaseAgent
from config.settings import EXPIRY_THRESHOLD_DAYS

class ExpiryAgent(BaseAgent):
    """Priority 1: Critical - Detects items nearing expiry."""
    def __init__(self):
        super().__init__("ExpiryAgent", "analysis", 1)

    def evaluate(self, context):
        row = context.inventory_data
        if row['Days_To_Expiry'] < EXPIRY_THRESHOLD_DAYS:
            alert = {
                "type": "EXPIRY",
                "priority": self.priority,
                "message": "Item is approaching expiry date."
            }
            context.risk_flags["EXPIRY"] = alert
            return alert
        return None
