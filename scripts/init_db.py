import sqlite3
import os
import json

def init_db(db_path='database/inventory.db'):
    """
    Initializes the SQLite database with the required schema.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            Item_ID INTEGER PRIMARY KEY,
            Item_Name TEXT,
            Category TEXT,
            Stock_Quantity INTEGER,
            Min_Stock_Level INTEGER,
            Cost_Per_Unit REAL,
            Expiry_Date TEXT,
            Last_Sold_Date TEXT,
            Avg_Daily_Usage REAL,
            Supplier_Name TEXT
        )
    """)

    # 2. Action Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT,
            quantity INTEGER,
            action_type TEXT,
            status TEXT,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Decision Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decision_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT,
            stockout_days REAL,
            reorder_qty INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 4. Performance Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER,
            score TEXT,
            comment TEXT,
            eval_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(decision_id) REFERENCES decision_logs(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()
