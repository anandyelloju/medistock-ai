from ..data.database_manager import DatabaseManager
from config.settings import SAFETY_BUFFER_DAYS

class AdaptiveOptimizer:
    """
    Core optimization engine that tunes reorder parameters based on historical performance.
    Ensures that the system 'learns' from past forecasting errors.
    """
    def __init__(self):
        self.db = DatabaseManager()

    def get_tuned_parameters(self, medicine_name):
        """
        Returns adjusted buffer days and quantity multipliers based on performance history.
        """
        history = self.db.get_performance_history(medicine_name, limit=3)
        
        # Default starting points
        tuned_buffer = SAFETY_BUFFER_DAYS
        tuned_multiplier = 1.0

        if history.empty:
            return tuned_buffer, tuned_multiplier

        # Scoring: GOOD=0, AVERAGE=1, POOR=2
        # If we have POOR scores, we increase the safety margin
        poor_count = len(history[history['score'] == 'POOR'])
        good_count = len(history[history['score'] == 'GOOD'])

        if poor_count >= 2:
            # Under-prediction detected: Increase safety net
            tuned_buffer += 5
            tuned_multiplier = 1.3
        elif good_count == 3:
            # High accuracy detected: Optimize for cost (lean inventory)
            tuned_buffer = max(2, tuned_buffer - 2)
            tuned_multiplier = 0.9

        # Safety Limits (Clamps)
        tuned_buffer = max(2, min(tuned_buffer, 25))
        tuned_multiplier = max(0.8, min(tuned_multiplier, 2.0))

        return tuned_buffer, tuned_multiplier
