from dataclasses import dataclass, field
from typing import Dict, Any

from .crystal_structure import PerovskiteStructure
from .electronic_properties import ElectronicProperties
from .optical_properties import OpticalProperties

@dataclass
class SolarCellDevice:
    """Represents a complete perovskite solar cell device."""
    perovskite_layer: PerovskiteStructure
    electronic_properties: ElectronicProperties
    optical_properties: OpticalProperties
    architecture: str = "n-i-p"
    layers: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.layers:
            self.layers = self._default_layers()

    def _default_layers(self) -> Dict[str, Any]:
        """Provides a default device architecture."""
        if self.architecture == "n-i-p":
            return {
                "ETL": {"material": "TiO2", "thickness": 50e-9}, # Electron Transport Layer
                "Perovskite": {"material": self.perovskite_layer.composition, "thickness": 500e-9},
                "HTL": {"material": "Spiro-OMeTAD", "thickness": 200e-9}, # Hole Transport Layer
            }
        else: # p-i-n
            return {
                "HTL": {"material": "PEDOT:PSS", "thickness": 40e-9},
                "Perovskite": {"material": self.perovskite_layer.composition, "thickness": 500e-9},
                "ETL": {"material": "PCBM", "thickness": 60e-9},
            }

    def __repr__(self) -> str:
        return f"SolarCellDevice(architecture='{self.architecture}', perovskite='{self.perovskite_layer.composition}')"