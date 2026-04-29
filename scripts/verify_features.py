import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd()))

from src.core.decision_engine import evaluate_row
from src.data.database_manager import DatabaseManager
import pandas as pd

def verify():
    db = DatabaseManager()
    print("--- 1. Testing Database Connection ---")
    inv = db.get_all_inventory()
    print(f"Total items in inventory: {len(inv)}")
    
    if inv.empty:
        print("Inventory empty. Please run load_demo_data.py first.")
        return

    # Pick the first item
    item = inv.iloc[0]
    print(f"\n--- 2. Testing Orchestration Flow for {item['Item_Name']} ---")
    
    # Process data to add calculated fields
    from src.core.data_processing import process_data
    df_processed = process_data(pd.DataFrame([item]))
    row = df_processed.iloc[0]
    
    # Run Agent Flow (Automation OFF)
    ctx = evaluate_row(row, automation_enabled=False)
    
    print("\n[PHASE: ANALYSIS]")
    print(f"Risk Flags: {ctx.risk_flags}")
    
    print("\n[PHASE: DECISION]")
    print(f"Execution Plan: {ctx.decisions.get('EXECUTION_PLAN', {}).get('message', 'NONE')}")
    print(f"Supplier Selection: {ctx.decisions.get('SUPPLIER_SELECTION', {}).get('message', 'NONE')}")
    
    print("\n[PHASE: EXECUTION]")
    print(f"Actions: {ctx.actions}")
    
    # Verify DB Logs
    print("\n--- 3. Verifying Persistence ---")
    decisions = db._execute_query("SELECT * FROM decision_logs ORDER BY id DESC LIMIT 1")
    print(f"Latest Decision Logged: {decisions.to_dict('records')}")
    
    # Test Performance Evaluation
    from src.agents.performance_evaluation_agent import PerformanceEvaluationAgent
    eval_agent = PerformanceEvaluationAgent()
    eval_results = eval_agent.evaluate()
    print(f"\n[PHASE: EVALUATION]")
    print(f"Evaluation Results: {eval_results}")
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify()
