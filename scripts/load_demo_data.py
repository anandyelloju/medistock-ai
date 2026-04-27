import sqlite3
import os
from datetime import datetime, timedelta

def load_demo_data(db_path='database/inventory.db'):
    """
    Populates the database with a realistic pharmacy demo dataset.
    """
    if not os.path.exists(db_path):
        from init_db import init_db
        init_db(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Clear existing data for a clean demo
    cursor.execute("DELETE FROM inventory")

    # Sample Data
    # Item_ID, Item_Name, Category, Stock_Quantity, Min_Stock_Level, Cost_Per_Unit, Expiry_Date, Avg_Daily_Usage, Supplier_Name
    demo_items = [
        (101, "Insulin Glargine", "Antidiabetic", 15, 20, 45.00, (datetime.now() + timedelta(days=400)).strftime('%Y-%m-%d'), 2.5, "LifeSync Pharma"),
        (102, "Amoxicillin 500mg", "Antibiotics", 120, 50, 12.50, (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'), 5.0, "RapidCure Supplies"),
        (103, "Paracetamol 650mg", "Analgesics", 500, 100, 2.50, (datetime.now() + timedelta(days=730)).strftime('%Y-%m-%d'), 15.0, "QuickRelief"),
        (104, "Metformin 500mg", "Antidiabetic", 8, 30, 8.00, (datetime.now() + timedelta(days=500)).strftime('%Y-%m-%d'), 4.0, "BulkMeds Co."),
        (105, "Atorvastatin 20mg", "Cardiovascular", 40, 60, 22.00, (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), 1.2, "StandardPharma"),
        (106, "Lisinopril 10mg", "Cardiovascular", 200, 50, 15.00, (datetime.now() + timedelta(days=600)).strftime('%Y-%m-%d'), 0.5, "General Medical"),
    ]

    cursor.executemany("""
        INSERT INTO inventory (Item_ID, Item_Name, Category, Stock_Quantity, Min_Stock_Level, Cost_Per_Unit, Expiry_Date, Avg_Daily_Usage, Supplier_Name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, demo_items)

    conn.commit()
    conn.close()
    print(f"Demo data successfully loaded into {db_path}")

if __name__ == "__main__":
    load_demo_data()
