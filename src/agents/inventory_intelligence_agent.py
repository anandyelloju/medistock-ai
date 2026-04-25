from .base_agent import BaseAgent
from config.settings import REORDER_BUFFER_DAYS

class InventoryIntelligenceAgent(BaseAgent):
    """
    Priority 1: Critical - Predictive agent that identifies stockout risks 
    based on average daily usage trends.
    """
    def __init__(self):
        super().__init__("InventoryIntelligenceAgent", 1)

    def evaluate(self, row):
        # The data_processing logic adds 'Days_Until_Stockout'
        # We check if this predictive metric is below our buffer threshold
        if row['Days_Until_Stockout'] < REORDER_BUFFER_DAYS:
            return {
                "type": "SMART_REORDER",
                "priority": self.priority,
                "message": f"Predicted stockout risk: Item will run out in {row['Days_Until_Stockout']} days."
            }
        return None
