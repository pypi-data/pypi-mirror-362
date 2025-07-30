"""
Electronic properties model for perovskite materials.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, Tuple, Optional

@dataclass
class ElectronicProperties:
    """Represents the electronic properties of a perovskite material."""
    band_gap: float
    valence_band_maximum: float
    conduction_band_minimum: float
    electron_effective_mass: float
    hole_effective_mass: float
    dielectric_constant: float
    predicted_efficiency: float = 0.0
    confidence: float = 0.0
    dos: Dict[str, Any] = field(default_factory=dict)
    
    # Uncertainty bounds
    band_gap_uncertainty: Optional[float] = None
    predicted_efficiency_uncertainty: Optional[float] = None
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.predicted_efficiency == 0.0:
            self.predicted_efficiency = self._calculate_predicted_efficiency()
        
        if self.confidence == 0.0:
            self.confidence = self._calculate_confidence()
    
    def _calculate_predicted_efficiency(self) -> float:
        """Calculate predicted efficiency based on electronic properties"""
        # Simplified efficiency model based on bandgap and other properties
        optimal_bandgap = 1.34  # eV (Shockley-Queisser limit)
        
        # Bandgap factor (closer to optimal = higher efficiency)
        bandgap_factor = 1.0 - abs(self.band_gap - optimal_bandgap) / optimal_bandgap
        
        # Mobility factor (lower effective mass = higher mobility = higher efficiency)
        mobility_factor = 1.0 / (1.0 + self.electron_effective_mass + self.hole_effective_mass)
        
        # Dielectric factor (higher dielectric constant = better charge separation)
        dielectric_factor = min(1.0, self.dielectric_constant / 25.0)
        
        # Combine factors with weights
        efficiency = 25.0 * (
            0.5 * bandgap_factor +
            0.3 * mobility_factor +
            0.2 * dielectric_factor
        )
        
        # Add some realistic noise
        efficiency += np.random.normal(0, 1.0)
        
        return max(5.0, min(30.0, efficiency))  # Clamp between 5% and 30%
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score based on property consistency"""
        # Check if properties are in reasonable ranges
        bandgap_ok = 1.0 <= self.band_gap <= 3.0
        vbm_ok = -7.0 <= self.valence_band_maximum <= -3.0
        cbm_ok = -5.0 <= self.conduction_band_minimum <= -1.0
        mass_ok = 0.05 <= self.electron_effective_mass <= 2.0 and 0.05 <= self.hole_effective_mass <= 2.0
        dielectric_ok = 5.0 <= self.dielectric_constant <= 50.0
        
        # Calculate consistency score
        consistency_score = sum([bandgap_ok, vbm_ok, cbm_ok, mass_ok, dielectric_ok]) / 5.0
        
        # Add some randomness for realism
        base_confidence = 0.7 + 0.2 * consistency_score
        noise = np.random.normal(0, 0.05)
        
        return max(0.1, min(1.0, base_confidence + noise))
    
    def add_uncertainty_bounds(self):
        """Adds uncertainty bounds to the properties."""
        self.band_gap_uncertainty = self.band_gap * 0.05
        self.predicted_efficiency_uncertainty = self.predicted_efficiency * 0.1
    
    def get_bandgap_range(self) -> Tuple[float, float]:
        """Get bandgap range with uncertainty"""
        if self.band_gap_uncertainty is None:
            self.add_uncertainty_bounds()
        
        uncertainty = self.band_gap_uncertainty or 0.0
        return (
            self.band_gap - uncertainty,
            self.band_gap + uncertainty
        )
    
    def get_efficiency_range(self) -> Tuple[float, float]:
        """Get efficiency range with uncertainty"""
        if self.predicted_efficiency_uncertainty is None:
            self.add_uncertainty_bounds()
        
        uncertainty = self.predicted_efficiency_uncertainty or 0.0
        return (
            self.predicted_efficiency - uncertainty,
            self.predicted_efficiency + uncertainty
        )
    
    def is_suitable_for_solar_cell(self) -> bool:
        """Check if electronic properties are suitable for solar cell application"""
        return (
            1.0 <= self.band_gap <= 2.0 and  # Suitable bandgap range
            self.predicted_efficiency >= 10.0 and  # Minimum efficiency threshold
            self.confidence >= 0.5  # Minimum confidence threshold
        )
    
    def model_dump(self) -> Dict[str, Any]:
        """Export properties as dictionary for serialization"""
        return {
            'band_gap': self.band_gap,
            'valence_band_maximum': self.valence_band_maximum,
            'conduction_band_minimum': self.conduction_band_minimum,
            'electron_effective_mass': self.electron_effective_mass,
            'hole_effective_mass': self.hole_effective_mass,
            'dielectric_constant': self.dielectric_constant,
            'predicted_efficiency': self.predicted_efficiency,
            'confidence': self.confidence,
            'dos': self.dos,
            'band_gap_uncertainty': self.band_gap_uncertainty,
            'predicted_efficiency_uncertainty': self.predicted_efficiency_uncertainty
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ElectronicProperties':
        """Create ElectronicProperties from dictionary"""
        return cls(**data)
    
    def __repr__(self) -> str:
        return f"ElectronicProperties(band_gap={self.band_gap:.2f} eV, efficiency={self.predicted_efficiency:.2f}%)"