from dataclasses import dataclass
from typing import Dict, Any

from .crystal_structure import PerovskiteStructure

@dataclass
class CostAnalysis:
    """Represents a cost analysis for a perovskite material."""
    composition: str
    precursor_costs: Dict[str, float]
    total_cost_per_gram: float

    @classmethod
    def from_composition(cls, composition: str, precursor_database: Any) -> "CostAnalysis":
        """Creates a CostAnalysis from a composition string."""
        precursors = PerovskiteStructure.parse_precursors(composition)
        precursor_costs = {
            precursor: precursor_database.get_cost(precursor) for precursor in precursors
        }
        total_cost = sum(precursor_costs.values())
        return cls(
            composition=composition,
            precursor_costs=precursor_costs,
            total_cost_per_gram=total_cost,
        )