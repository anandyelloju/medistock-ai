from ..data.supplier_data import SUPPLIERS

class SupplierManager:
    """
    Simulates supplier selection based on business rules.
    Optimizes for Speed (Delivery Days) during emergencies and Cost (Price) during normal replenishment.
    """
    @staticmethod
    def get_best_supplier(medicine_name, category, urgency):
        """
        Selects the most suitable supplier based on the item's current state.
        """
        # 1. Fetch suppliers for the category (fallback to Default)
        options = SUPPLIERS.get(category, SUPPLIERS["Default"])
        
        # 2. Selection Logic
        if "CRITICAL" in urgency or "HIGH" in urgency:
            # URGENT: Prioritize shortest delivery time
            best = min(options, key=lambda x: x['delivery_days'])
            reason = "Prioritized shortest delivery time due to urgency."
        else:
            # NORMAL: Prioritize lowest price
            best = min(options, key=lambda x: x['price_per_unit'])
            reason = "Prioritized lowest cost for routine replenishment."
            
        return {
            "supplier_name": best['name'],
            "price": best['price_per_unit'],
            "delivery_days": best['delivery_days'],
            "selection_reason": reason
        }
