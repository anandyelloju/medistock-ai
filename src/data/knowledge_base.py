import json
import os

class MedicineKnowledgeBase:
    """
    A simple retrieval system for medicine-specific domain knowledge.
    Loads data from the JSON knowledge base and provides context for agents.
    """
    def __init__(self, file_path='database/medicine_knowledge.json'):
        self.file_path = file_path
        self.knowledge = {}
        self._load_knowledge()

    def _load_knowledge(self):
        """Loads the JSON file into a searchable dictionary."""
        if not os.path.exists(self.file_path):
            print(f"Warning: Knowledge base not found at {self.file_path}")
            return

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                # Store by name for O(1) lookup
                self.knowledge = {item['medicine_name'].lower(): item for item in data}
        except Exception as e:
            print(f"Error loading knowledge base: {e}")

    def get_medicine_context(self, medicine_name):
        """
        Retrieves context for a specific medicine.
        Returns a dictionary of metadata or a default structure if not found.
        """
        if not medicine_name:
            return self._get_default_context()

        # Case-insensitive lookup
        item = self.knowledge.get(medicine_name.lower())
        
        if item:
            return {
                "category": item.get("category", "General"),
                "criticality": item.get("criticality", "Medium"),
                "seasonal_info": item.get("seasonal_demand", "Steady"),
                "has_substitute": item.get("substitute_available", "Unknown")
            }
        
        return self._get_default_context()

    def _get_default_context(self):
        """Standard fallback context for missing items."""
        return {
            "category": "General Medication",
            "criticality": "Medium",
            "seasonal_info": "Steady",
            "has_substitute": "Unknown"
        }

# Global singleton instance for easy access across agents
kb = MedicineKnowledgeBase()
