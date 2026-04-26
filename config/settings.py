# Centralized Configuration for MediStock AI Inventory Rules

# Threshold for near-expiry alerts (Critical Priority)
EXPIRY_THRESHOLD_DAYS = 60

# Threshold for dead stock alerts (Info Priority)
DEAD_STOCK_DAYS = 180

# Predictive Alert Threshold
REORDER_BUFFER_DAYS = 10

# Supply Chain Parameters
LEAD_TIME_DAYS = 7        # Time taken for stock to arrive
SAFETY_BUFFER_DAYS = 3     # Safety margin for demand spikes
