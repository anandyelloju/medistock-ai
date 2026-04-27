import sqlite3
import pandas as pd
import os

class DatabaseManager:
    """
    Handles all SQLite database interactions for the MediStock AI system.
    Designed for efficiency and compatibility with pandas.
    """
    def __init__(self, db_path='database/inventory.db'):
        self.db_path = db_path
        
    def _execute_query(self, query, params=()):
        """Internal helper to run queries and return a DataFrame."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at {self.db_path}. Please run migration first.")
            
        with sqlite3.connect(self.db_path) as conn:
            # We return a DataFrame as it's most efficient for Streamlit and data processing
            return pd.read_sql_query(query, conn, params=params)

    def get_all_inventory(self):
        """Fetches the entire inventory table."""
        return self._execute_query("SELECT * FROM inventory")

    def get_low_stock(self, threshold=None):
        """
        Fetches items where stock is below threshold.
        If threshold is None, uses the item's own Min_Stock_Level.
        """
        if threshold is not None:
            query = "SELECT * FROM inventory WHERE Stock_Quantity < ?"
            return self._execute_query(query, params=(threshold,))
        else:
            query = "SELECT * FROM inventory WHERE Stock_Quantity < Min_Stock_Level"
            return self._execute_query(query)

    def log_action(self, medicine_name, quantity, action_type, status, details=None):
        """
        Logs an automated action (e.g., PO generation) into the SQLite database.
        Creates the 'action_logs' table if it does not already exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Ensure logs table exists
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
            # Insert log entry
            cursor.execute("""
                INSERT INTO action_logs (medicine_name, quantity, action_type, status, details)
                VALUES (?, ?, ?, ?, ?)
            """, (medicine_name, quantity, action_type, status, details))
            conn.commit()

    def get_action_logs(self, limit=10):
        """Fetches the most recent action logs."""
        query = "SELECT * FROM action_logs ORDER BY timestamp DESC LIMIT ?"
        try:
            return self._execute_query(query, params=(limit,))
        except Exception:
            # If table doesn't exist yet, return an empty DataFrame with correct columns
            return pd.DataFrame(columns=['id', 'medicine_name', 'quantity', 'action_type', 'status', 'details', 'timestamp'])
