from ..agents import (
    ReorderAgent, ExpiryAgent, DeadStockAgent, 
    InventoryIntelligenceAgent, ReorderExecutionAgent, 
    ActionExecutionAgent, CoordinatorAgent
)
from ..data.knowledge_base import kb

# Initialize agents
agents_suite = [
    ExpiryAgent(),
    DeadStockAgent(),
    InventoryIntelligenceAgent(),
    ReorderExecutionAgent(),
    ActionExecutionAgent(),
    ReorderAgent()
]

# Initialize the Coordinator
coordinator = CoordinatorAgent(agents_suite)

def evaluate_row(row):
    """
    Evaluates an inventory item using the Coordinator Agent orchestration.
    The flow is managed dynamically: Analysis -> Decision -> Execution.
    """
    # Fetch domain context for the current item
    context = kb.get_medicine_context(row['Item_Name'])

    # Delegate orchestration to the Coordinator
    return coordinator.orchestrate(row, context=context)