from .base_agent import BaseAgent
from ..core.action_manager import generate_purchase_order
from ..core.email_manager import send_purchase_order_email
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

    def evaluate(self, context):
        """
        Executes an action plan if it meets high-urgency criteria.
        Read plan from context.decisions.
        """
        row = context.inventory_data
        plan = context.decisions.get('EXECUTION_PLAN')

        if not plan:
            return None

        medicine_name = row['Item_Name']
        urgency = plan.get('urgency', '')

        # Trigger Criteria: Only for CRITICAL or HIGH urgency
        if "CRITICAL" in urgency or "HIGH" in urgency:
            
            # 1. Memory-based Deduplication (Current Session)
            if medicine_name in self.executed_items:
                alert = {
                    "type": "ACTION_LOG",
                    "priority": 3,
                    "status": "SKIPPED",
                    "message": f"Action for {medicine_name} already logged in this session."
                }
                context.actions["ACTION_LOG"] = alert
                return alert

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
                
                # 3. Email Dispatch
                email_status = send_purchase_order_email(file_path)
                email_note = " and dispatched via email" if email_status else " (Email dispatch skipped/failed)"
                
                # Persistent DB Logging
                self.db.log_action(
                    medicine_name=medicine_name,
                    quantity=plan.get('reorder_qty', 0),
                    action_type="PO_GENERATION",
                    status="SUCCESS",
                    details=f"{file_path} | Email: {email_status}"
                )
                
                alert = {
                    "type": "ACTION_LOG",
                    "priority": 3, # Info level for logs
                    "status": "EXECUTED",
                    "message": f"✅ Purchase Order generated for {medicine_name}{email_note}.",
                    "file_path": file_path
                }
                context.actions["ACTION_LOG"] = alert
                return alert
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
                
                alert = {
                    "type": "ACTION_LOG",
                    "priority": 1, # Critical if execution fails
                    "status": "FAILED",
                    "message": f"❌ Failed to generate Purchase Order for {medicine_name}."
                }
                context.actions["ACTION_LOG"] = alert
                return alert

        return None
