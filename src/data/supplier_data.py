# Mock Supplier Database for Simulation
# Key: Medicine Category or Name
# Value: List of available suppliers with their specific metrics

SUPPLIERS = {
    "Antidiabetic": [
        {"name": "LifeSync Pharma", "price_per_unit": 42.50, "delivery_days": 2, "rating": 4.8},
        {"name": "BulkMeds Co.", "price_per_unit": 38.00, "delivery_days": 6, "rating": 4.2}
    ],
    "Antibiotics": [
        {"name": "RapidCure Supplies", "price_per_unit": 12.00, "delivery_days": 3, "rating": 4.5},
        {"name": "GlobalGeneric", "price_per_unit": 9.50, "delivery_days": 8, "rating": 4.0}
    ],
    "Analgesics": [
        {"name": "QuickRelief", "price_per_unit": 5.00, "delivery_days": 1, "rating": 4.9},
        {"name": "StandardPharma", "price_per_unit": 4.20, "delivery_days": 4, "rating": 4.3}
    ],
    "Default": [
        {"name": "General Medical", "price_per_unit": 20.00, "delivery_days": 4, "rating": 4.0},
        {"name": "ExpressHealth", "price_per_unit": 25.00, "delivery_days": 2, "rating": 4.5}
    ]
}
