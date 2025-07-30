from typing import List, Dict, Any

class ActiveLearningLoop:
    """Class for managing the active learning loop."""
    def __init__(self, model, uncertainty_estimator):
        self.model = model
        self.uncertainty_estimator = uncertainty_estimator

    def select_next_experiments(self, candidates: List[Dict[str, Any]], n_experiments: int) -> List[Dict[str, Any]]:
        """Selects the next experiments to perform based on model uncertainty."""
        uncertainties = [
            self.uncertainty_estimator.get_uncertainty(c)["prediction_std"] for c in candidates
        ]
        
        # Select candidates with the highest uncertainty
        sorted_indices = sorted(range(len(uncertainties)), key=lambda k: uncertainties[k], reverse=True)
        
        return [candidates[i] for i in sorted_indices[:n_experiments]]