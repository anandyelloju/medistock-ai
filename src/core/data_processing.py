import pandas as pd
from datetime import datetime

def process_data(df):
    # Ensure date columns are proper datetime objects (crucial for SQLite inputs)
    df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'])
    df['Last_Sold_Date'] = pd.to_datetime(df['Last_Sold_Date'])
    
    today = pd.to_datetime(datetime.today())

    df['Days_To_Expiry'] = (df['Expiry_Date'] - today).dt.days
    df['Days_Since_Last_Sale'] = (today - df['Last_Sold_Date']).dt.days
    
    # Demand Forecasting - Avg_Daily_Usage is already in the table
    
    # Calculate days until stockout, handling zero usage cases
    df['Days_Until_Stockout'] = df.apply(
        lambda x: x['Stock_Quantity'] / x['Avg_Daily_Usage'] if x['Avg_Daily_Usage'] > 0 else 999,
        axis=1
    ).round(1)

    return df