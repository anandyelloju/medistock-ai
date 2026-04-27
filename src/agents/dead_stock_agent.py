from .base_agent import BaseAgent
from config.settings import DEAD_STOCK_DAYS

class DeadStockAgent(BaseAgent):
    """Priority 3: Info - Detects slow-moving inventory."""
    def __init__(self):
        super().__init__("DeadStockAgent", "analysis", 3)

    def evaluate(self, context):
        row = context.inventory_data
        if row['Days_Since_Last_Sale'] > DEAD_STOCK_DAYS:
            alert = {
                "type": "DEAD_STOCK",
                "priority": self.priority,
                "message": "No recent sales recorded (Dead Stock)."
            }
            context.risk_flags["DEAD_STOCK"] = alert
            return alert
        return None
