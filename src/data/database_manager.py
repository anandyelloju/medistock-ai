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
    def log_decision(self, medicine_name, stockout_days, reorder_qty):
        """
        Logs a reorder decision into the SQLite database.
        Prevents duplicates by checking for existing identical decisions on the same day.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS decision_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medicine_name TEXT,
                    stockout_days REAL,
                    reorder_qty INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Simple deduplication: Check if this item has a decision in the last 12 hours
            cursor.execute("""
                SELECT id FROM decision_logs 
                WHERE medicine_name = ? AND timestamp > datetime('now', '-12 hours')
            """, (medicine_name,))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO decision_logs (medicine_name, stockout_days, reorder_qty)
                    VALUES (?, ?, ?)
                """, (medicine_name, stockout_days, reorder_qty))
    def log_performance_eval(self, decision_id, score, comment):
        """Logs the performance score of a past decision."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
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
            cursor.execute("""
                INSERT INTO performance_logs (decision_id, score, comment)
                VALUES (?, ?, ?)
            """, (decision_id, score, comment))
            conn.commit()

    def get_pending_evaluations(self):
        """Fetches decisions that haven't been evaluated yet."""
        query = """
            SELECT d.* FROM decision_logs d
            LEFT JOIN performance_logs p ON d.id = p.decision_id
            WHERE p.id IS NULL
        """
        try:
            return self._execute_query(query)
    def get_performance_history(self, medicine_name, limit=5):
        """Fetches the performance history for a specific medicine."""
        query = """
            SELECT p.score, p.eval_timestamp FROM performance_logs p
            JOIN decision_logs d ON p.decision_id = d.id
            WHERE d.medicine_name = ?
            ORDER BY p.eval_timestamp DESC
            LIMIT ?
        """
        try:
            return self._execute_query(query, params=(medicine_name, limit))
        except Exception:
            return pd.DataFrame()
