# Centralized Configuration for MediStock AI Inventory Rules

# Threshold for near-expiry alerts (Critical Priority)
EXPIRY_THRESHOLD_DAYS = 60

# Threshold for dead stock alerts (Info Priority)
# Items with no sales for more than this many days are flagged
DEAD_STOCK_DAYS = 180

# Buffer added to the minimum stock level for reorder alerts (Warning Priority)
# Set to 0 to maintain current behavior (reorder when below Min_Stock_Level)
REORDER_BUFFER_DAYS = 0
