from ..agents import (
    ReorderAgent, ExpiryAgent, DeadStockAgent, 
    InventoryIntelligenceAgent, ReorderExecutionAgent, 
    ActionExecutionAgent, CoordinatorAgent, SupplierSelectionAgent
)
from ..data.knowledge_base import kb

# Initialize agents
agents_suite = [
    ExpiryAgent(),
    DeadStockAgent(),
    InventoryIntelligenceAgent(),
    ReorderExecutionAgent(),
    SupplierSelectionAgent(),
    ActionExecutionAgent(),
    ReorderAgent()
]

# Initialize the Coordinator
coordinator = CoordinatorAgent(agents_suite)

def evaluate_row(row):
    """
    Evaluates an inventory item using the Coordinator Agent orchestration.
    Returns the full SharedContext for UI visualization.
    """
    # Fetch domain context for the current item
    context = kb.get_medicine_context(row['Item_Name'])

    # Initialize context and orchestrate
    return coordinator.orchestrate_with_context(row, domain_knowledge=context)