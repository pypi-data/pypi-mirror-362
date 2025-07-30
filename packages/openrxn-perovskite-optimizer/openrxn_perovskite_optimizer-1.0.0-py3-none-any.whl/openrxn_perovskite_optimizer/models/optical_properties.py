from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class OpticalProperties:
    """Represents the optical properties of a perovskite material."""
    absorption_spectrum: Dict[str, Any] = field(default_factory=dict)
    refractive_index: Dict[str, Any] = field(default_factory=dict)
    extinction_coefficient: float = 0.0
    photoluminescence_quantum_yield: float = 0.0
    photoluminescence_lifetime: float = 0.0

    def __repr__(self) -> str:
        return f"OpticalProperties(plqy={self.photoluminescence_quantum_yield:.2f})"