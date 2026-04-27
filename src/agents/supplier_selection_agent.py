from .base_agent import BaseAgent
from ..core.supplier_manager import SupplierManager

class SupplierSelectionAgent(BaseAgent):
    """
    Role: decision - Specialized agent for choosing the best procurement partner.
    Determines the specific supplier for a reorder plan based on urgency vs cost.
    """
    def __init__(self):
        super().__init__("SupplierSelectionAgent", "decision", 2, dependencies=["ReorderExecutionAgent"])

    def evaluate(self, context):
        """
        Analyzes the execution plan and selects a supplier.
        """
        row = context.inventory_data
        kb_ctx = context.domain_knowledge
        # We need the execution plan from the previous decision agent
        plan = context.decisions.get('EXECUTION_PLAN')

        if not plan:
            return None

        # Delegate selection to the specialized manager
        supplier_info = SupplierManager.get_best_supplier(
            row['Item_Name'],
            kb_ctx.get('category', 'Default'),
            plan.get('urgency', 'NORMAL')
        )

        alert = {
            "type": "SUPPLIER_SELECTION",
            "priority": self.priority,
            "message": f"Selected Supplier: {supplier_info['supplier_name']}. Reasoning: {supplier_info['selection_reason']}",
            "supplier": supplier_info['supplier_name'],
            "price": supplier_info['price'],
            "delivery_days": supplier_info['delivery_days']
        }
        
        # Write back to shared context
        context.decisions["SUPPLIER_SELECTION"] = alert
        return alert
