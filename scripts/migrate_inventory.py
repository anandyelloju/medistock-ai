import pandas as pd
import sqlite3
import os

# Configuration
CSV_FILE = 'data/inventory.csv'
DB_FILE = 'data/inventory.db'
TABLE_NAME = 'inventory'

def migrate_data():
    """
    Migrates pharmacy inventory data from CSV to SQLite.
    Ensures date formats are preserved and table is refreshed.
    """
    print("--- Initializing MediStock AI Data Migration ---")

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    # Check if source CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: Source file '{CSV_FILE}' not found.")
        return

    try:
        # 1. Load data using pandas
        print(f"Reading data from {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE)

        # 2. Critical: Convert Date columns to proper formats
        # We use errors='coerce' to handle any malformed dates gracefully
        print("Converting date columns...")
        df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce')
        df['Last_Sold_Date'] = pd.to_datetime(df['Last_Sold_Date'], errors='coerce')

        # 3. Establish Database Connection
        # Connect will create the file if it doesn't exist
        with sqlite3.connect(DB_FILE) as conn:
            print(f"Connected to database: {DB_FILE}")

            # 4. Migrate to SQLite
            # if_exists='replace' drops the old table and creates a fresh one
            # index=False prevents pandas from adding an extra index column
            df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

        # 5. Success Message
        print("\n" + "="*40)
        print("MIGRATION SUCCESSFUL")
        print(f"Total Rows Processed: {len(df)}")
        print(f"Table Created: {TABLE_NAME}")
        print(f"Database Saved: {DB_FILE}")
        print("="*40)

    except Exception as e:
        print(f"Critical Failure during migration: {e}")

if __name__ == "__main__":
    migrate_data()
