# Centralized Configuration for MediStock AI Inventory Rules

# Threshold for near-expiry alerts (Critical Priority)
EXPIRY_THRESHOLD_DAYS = 60

# Threshold for dead stock alerts (Info Priority)
# Items with no sales for more than this many days are flagged
DEAD_STOCK_DAYS = 180

# Buffer added to the minimum stock level for reorder alerts (Warning Priority)
# Set to 10 to enable predictive alerts (reorder when 10 days of stock left)
REORDER_BUFFER_DAYS = 10
