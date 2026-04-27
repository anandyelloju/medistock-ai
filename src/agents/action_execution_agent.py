from .base_agent import BaseAgent
from ..core.action_manager import generate_purchase_order
from ..data.database_manager import DatabaseManager
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ActionExecutionAgent")

class ActionExecutionAgent(BaseAgent):
    """
    Priority 1: Critical - Automates the transition from 'Planning' to 'Execution'.
    Responsible for generating formal Purchase Orders for high-urgency items.
    """
    def __init__(self):
        super().__init__("ActionExecutionAgent", "execution", 1, dependencies=["ReorderExecutionAgent"])
        self.executed_items = set() # Simple deduplication in memory for current session
        self.db = DatabaseManager()

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
            
            # 1. Memory-based Deduplication (Current Session)
            if medicine_name in self.executed_items:
                return {
                    "type": "ACTION_LOG",
                    "priority": 3,
                    "status": "SKIPPED",
                    "message": f"Action for {medicine_name} already logged in this session."
                }

            # 2. File-based Deduplication (Persistent)
            # Check if a PO for this item was already generated today
            export_dir = "database/exports"
            today_prefix = datetime.now().strftime("%Y%m%d")
            if os.path.exists(export_dir):
                existing_files = os.listdir(export_dir)
                # Check for files like PO_YYYYMMDD_*.csv that might contain this item
                # (Simple check: if any PO was generated today, we pause for safety or we could parse them)
                # For now, let's stick to the session-based and add a more descriptive message
                pass 


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
                
                # Persistent DB Logging
                self.db.log_action(
                    medicine_name=medicine_name,
                    quantity=plan.get('reorder_qty', 0),
                    action_type="PO_GENERATION",
                    status="SUCCESS",
                    details=file_path
                )
                
                return {
                    "type": "ACTION_LOG",
                    "priority": 3, # Info level for logs
                    "status": "EXECUTED",
                    "message": f"✅ Purchase Order generated for {medicine_name}.",
                    "file_path": file_path
                }
            else:
                logger.error(f"FAILURE: Could not generate Purchase Order for {medicine_name}")
                
                # Persistent DB Logging
                self.db.log_action(
                    medicine_name=medicine_name,
                    quantity=plan.get('reorder_qty', 0),
                    action_type="PO_GENERATION",
                    status="FAILURE",
                    details="File system error"
                )
                
                return {
                    "type": "ACTION_LOG",
                    "priority": 1, # Critical if execution fails
                    "status": "FAILED",
                    "message": f"❌ Failed to generate Purchase Order for {medicine_name}."
                }

        return None
