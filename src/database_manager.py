import sqlite3
import pandas as pd
import os

class DatabaseManager:
    """
    Handles all SQLite database interactions for the MediStock AI system.
    Designed for efficiency and compatibility with pandas.
    """
    def __init__(self, db_path='data/inventory.db'):
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

    def get_near_expiry(self, days=60):
        """Fetches items expiring within the specified number of days."""
        # SQLite date comparison
        query = "SELECT * FROM inventory WHERE Expiry_Date <= date('now', ?)"
        param = f"+{days} days"
        return self._execute_query(query, params=(param,))
