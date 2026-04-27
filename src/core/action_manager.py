import pandas as pd
import os
from datetime import datetime

def generate_purchase_order(reorder_plan):
    """
    Generates a Purchase Order (PO) file based on a reorder plan.
    Saves the output as a CSV file in the 'database/exports/' directory.
    """
    if not reorder_plan:
        return None

    # Create export directory if it doesn't exist
    export_dir = "database/exports"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # Prepare data for CSV
    # The reorder_plan can be a list of plan objects or a single one
    if isinstance(reorder_plan, dict):
        reorder_plan = [reorder_plan]

    po_data = []
    for plan in reorder_plan:
        po_data.append({
            "Medicine_Name": plan.get("medicine", "Unknown"),
            "Quantity": plan.get("reorder_qty", 0),
            "Urgency": plan.get("urgency", "Normal"),
            "Generated_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Create DataFrame
    df_po = pd.DataFrame(po_data)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"PO_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)

    # Save to CSV
    try:
        df_po.to_csv(filepath, index=False)
        return filepath
    except Exception as e:
        print(f"Error generating PO: {e}")
        return None
