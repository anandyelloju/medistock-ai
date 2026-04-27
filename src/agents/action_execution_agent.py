from .base_agent import BaseAgent
from ..core.action_manager import generate_purchase_order
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ActionExecutionAgent")

class ActionExecutionAgent(BaseAgent):
    """
    Priority 1: Critical - Automates the transition from 'Planning' to 'Execution'.
    Responsible for generating formal Purchase Orders for high-urgency items.
    """
    def __init__(self):
        super().__init__("ActionExecutionAgent", 1)
        self.executed_items = set() # Simple deduplication in memory for current session

    def evaluate(self, row, context=None, plan=None):
        """
        Executes an action plan if it meets high-urgency criteria.
        Expects a 'plan' dictionary containing reorder details.
        """
        if not plan:
            return None

        medicine_name = row['Item_Name']
        urgency = plan.get('urgency', '')

        # Trigger Criteria: Only for CRITICAL or HIGH urgency
        if "CRITICAL" in urgency or "HIGH" in urgency:
            
            # Simple Deduplication: Don't execute the same item twice in one session
            if medicine_name in self.executed_items:
                return {
                    "type": "ACTION_LOG",
                    "priority": 3, # Info level for logs
                    "status": "SKIPPED",
                    "message": f"Action for {medicine_name} already executed in this session."
                }

            # Prepare data for PO
            po_plan = {
                "medicine": medicine_name,
                "reorder_qty": plan.get('reorder_qty', 0),
                "urgency": urgency
            }

            # Execute: Generate PO
            file_path = generate_purchase_order(po_plan)

            if file_path:
                self.executed_items.add(medicine_name)
                logger.info(f"SUCCESS: Generated Purchase Order for {medicine_name} at {file_path}")
                
                return {
                    "type": "ACTION_LOG",
                    "priority": 3, # Info level for logs
                    "status": "EXECUTED",
                    "message": f"✅ Purchase Order generated for {medicine_name}.",
                    "file_path": file_path
                }
            else:
                logger.error(f"FAILURE: Could not generate Purchase Order for {medicine_name}")
                return {
                    "type": "ACTION_LOG",
                    "priority": 1, # Critical if execution fails
                    "status": "FAILED",
                    "message": f"❌ Failed to generate Purchase Order for {medicine_name}."
                }

        return None
