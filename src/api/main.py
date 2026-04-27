from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..data.database_manager import DatabaseManager
from ..core.decision_engine import evaluate_row
from ..core.data_processing import process_data

app = FastAPI(title="MediStock AI API", description="Autonomous Inventory Orchestration Service")
db = DatabaseManager()

class ActionRequest(BaseModel):
    item_id: int
    automation_enabled: bool = False

@app.get("/")
def read_root():
    return {"message": "MediStock AI Backend is Online"}

@app.get("/analyze-inventory")
def analyze_inventory():
    """
    Analyzes the entire inventory and returns identified risks.
    """
    df = db.get_all_inventory()
    if df.empty:
        return {"status": "success", "data": [], "message": "Inventory is empty"}
    
    df = process_data(df)
    results = []
    
    for _, row in df.iterrows():
        ctx = evaluate_row(row, automation_enabled=False)
        alerts = ctx.get_all_alerts()
        if alerts:
            results.append({
                "item_name": row['Item_Name'],
                "alerts": alerts
            })
            
    return {"status": "success", "count": len(results), "data": results}

@app.post("/run-agent-flow/{item_id}")
def run_agent_flow(item_id: int, automation_enabled: bool = False):
    """
    Triggers the full multi-agent orchestration for a specific item.
    """
    df = db.get_all_inventory()
    item_row = df[df['Item_ID'] == item_id]
    
    if item_row.empty:
        raise HTTPException(status_code=404, detail="Item not found")
        
    row = process_data(item_row).iloc[0]
    ctx = evaluate_row(row, automation_enabled=automation_enabled)
    
    return {
        "status": "success",
        "item_name": row['Item_Name'],
        "orchestration": {
            "risks": ctx.risk_flags,
            "decisions": ctx.decisions,
            "actions": ctx.actions
        }
    }

@app.get("/inventory-stats")
def get_stats():
    """Returns high-level inventory metrics."""
    df = db.get_all_inventory()
    if df.empty:
        return {"total_items": 0, "total_value": 0}
        
    total_value = (df['Stock_Quantity'] * df['Cost_Per_Unit']).sum()
    return {
        "total_items": len(df),
        "total_value": float(total_value),
        "low_stock_count": int(len(df[df['Stock_Quantity'] < df['Min_Stock_Level']]))
    }
