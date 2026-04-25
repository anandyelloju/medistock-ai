from .base_agent import BaseAgent
from config.settings import DEAD_STOCK_DAYS

class DeadStockAgent(BaseAgent):
    """Priority 3: Info - Detects slow-moving inventory."""
    def __init__(self):
        super().__init__("DeadStockAgent", 3)

    def evaluate(self, row):
        if row['Days_Since_Last_Sale'] > DEAD_STOCK_DAYS:
            return {
                "type": "DEAD_STOCK",
                "priority": self.priority,
                "message": "No recent sales recorded (Dead Stock)."
            }
        return None
