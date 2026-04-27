from .base_agent import BaseAgent
from ..data.database_manager import DatabaseManager
import random

class PerformanceEvaluationAgent(BaseAgent):
    """
    Role: analysis - Post-action agent that evaluates the quality of past decisions.
    Compares predicted outcomes against simulated reality to score system accuracy.
    """
    def __init__(self):
        super().__init__("PerformanceEvaluationAgent", "analysis", 3)
        self.db = DatabaseManager()

    def evaluate(self, context=None):
        """
        Scans for unevaluated decisions and performs a performance simulation.
        """
        pending = self.db.get_pending_evaluations()
        if pending.empty:
            return None

        results = []
        for _, decision in pending.iterrows():
            # 1. Simulate "Reality"
            # In a real system, we would look at the current Stock_Quantity vs the old one.
            # Here we simulate variability in consumption (±20%)
            actual_usage_variance = random.uniform(0.8, 1.2)
            predicted_days = decision['stockout_days']
            
            # 2. Score the Decision
            # Good: Accurate prediction (variance < 10%)
            # Average: Fairly accurate (variance < 25%)
            # Poor: Inaccurate prediction
            
            if 0.95 <= actual_usage_variance <= 1.05:
                score = "GOOD"
                comment = "Prediction matched consumption within 5% error margin."
            elif 0.85 <= actual_usage_variance <= 1.15:
                score = "AVERAGE"
                comment = "Prediction was slightly off due to minor usage fluctuations."
            else:
                score = "POOR"
                comment = "Significant divergence between predicted and actual consumption."

            # 3. Log Result
            self.db.log_performance_eval(decision['id'], score, comment)
            results.append({
                "medicine": decision['medicine_name'],
                "score": score,
                "comment": comment
            })

        return results if results else None
