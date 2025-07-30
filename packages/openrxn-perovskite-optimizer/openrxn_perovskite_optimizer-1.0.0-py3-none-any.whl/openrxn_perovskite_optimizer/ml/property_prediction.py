"""
Property prediction models for perovskite materials.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import logging
from dataclasses import dataclass
from datetime import datetime

from ..models.crystal_structure import PerovskiteStructure
from ..models.electronic_properties import ElectronicProperties
from ..models.optical_properties import OpticalProperties

logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """Result from property prediction"""
    predicted_value: float
    uncertainty: float
    confidence: float
    model_version: str
    timestamp: datetime

class PropertyPredictor:
    """Machine learning models for predicting perovskite properties"""
    
    def __init__(self):
        self.models = {}
        self.model_versions = {}
        self.training_data = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models"""
        # Placeholder for actual ML models
        self.models = {
            "bandgap": self._create_bandgap_model(),
            "formation_energy": self._create_formation_energy_model(),
            "stability": self._create_stability_model(),
            "efficiency": self._create_efficiency_model()
        }
        
        self.model_versions = {
            "bandgap": "v1.0",
            "formation_energy": "v1.0", 
            "stability": "v1.0",
            "efficiency": "v1.0"
        }
    
    def _create_bandgap_model(self):
        """Create bandgap prediction model"""
        # Simplified model - in reality would use trained ML model
        def predict_bandgap(structure: PerovskiteStructure) -> Tuple[float, float]:
            composition = structure.composition
            
            # Basic composition-based prediction
            if "MAPbI3" in composition:
                bandgap = 1.55 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            elif "FAPbI3" in composition:
                bandgap = 1.48 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            elif "CsPbI3" in composition:
                bandgap = 1.73 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            else:
                # Generic prediction
                bandgap = 1.5 + np.random.normal(0, 0.1)
                uncertainty = 0.1
            
            return bandgap, uncertainty
        
        return predict_bandgap
    
    def _create_formation_energy_model(self):
        """Create formation energy prediction model"""
        def predict_formation_energy(structure: PerovskiteStructure) -> Tuple[float, float]:
            composition = structure.composition
            
            # Simplified formation energy calculation
            if "MAPbI3" in composition:
                formation_energy = -0.85 + np.random.normal(0, 0.1)
                uncertainty = 0.1
            elif "FAPbI3" in composition:
                formation_energy = -0.78 + np.random.normal(0, 0.1)
                uncertainty = 0.1
            elif "CsPbI3" in composition:
                formation_energy = -0.92 + np.random.normal(0, 0.1)
                uncertainty = 0.1
            else:
                formation_energy = -0.8 + np.random.normal(0, 0.15)
                uncertainty = 0.15
            
            return formation_energy, uncertainty
        
        return predict_formation_energy
    
    def _create_stability_model(self):
        """Create stability prediction model"""
        def predict_stability(structure: PerovskiteStructure) -> Tuple[float, float]:
            composition = structure.composition
            
            # Stability score (0-1)
            if "MAPbI3" in composition:
                stability = 0.75 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            elif "FAPbI3" in composition:
                stability = 0.65 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            elif "CsPbI3" in composition:
                stability = 0.85 + np.random.normal(0, 0.05)
                uncertainty = 0.05
            else:
                stability = 0.7 + np.random.normal(0, 0.1)
                uncertainty = 0.1
            
            stability = max(0, min(1, stability))
            return stability, uncertainty
        
        return predict_stability
    
    def _create_efficiency_model(self):
        """Create efficiency prediction model"""
        def predict_efficiency(structure: PerovskiteStructure) -> Tuple[float, float]:
            composition = structure.composition
            
            # Efficiency prediction based on composition
            if "MAPbI3" in composition:
                efficiency = 22.0 + np.random.normal(0, 2.0)
                uncertainty = 2.0
            elif "FAPbI3" in composition:
                efficiency = 24.0 + np.random.normal(0, 2.0)
                uncertainty = 2.0
            elif "CsPbI3" in composition:
                efficiency = 18.0 + np.random.normal(0, 2.0)
                uncertainty = 2.0
            else:
                efficiency = 20.0 + np.random.normal(0, 3.0)
                uncertainty = 3.0
            
            efficiency = max(5, min(30, efficiency))
            return efficiency, uncertainty
        
        return predict_efficiency
    
    async def predict_properties(self, structure: PerovskiteStructure) -> ElectronicProperties:
        """Predict electronic properties for a structure"""
        logger.info(f"Predicting properties for {structure.composition}")
        
        # Predict bandgap
        bandgap, bg_uncertainty = self.models["bandgap"](structure)
        
        # Predict formation energy
        formation_energy, fe_uncertainty = self.models["formation_energy"](structure)
        
        # Predict other electronic properties based on bandgap
        # VBM and CBM estimation
        vbm = -5.4 + np.random.normal(0, 0.2)  # eV vs vacuum
        cbm = vbm + bandgap
        
        # Effective masses (in units of electron mass)
        electron_mass = 0.1 + np.random.normal(0, 0.05)
        hole_mass = 0.15 + np.random.normal(0, 0.05)
        
        # Dielectric constant
        dielectric = 25.0 + np.random.normal(0, 3.0)
        
        # Calculate confidence based on uncertainties
        confidence = 1.0 - (bg_uncertainty + fe_uncertainty) / 2.0
        confidence = max(0.1, min(1.0, confidence))
        
        # Create electronic properties object
        properties = ElectronicProperties(
            band_gap=bandgap,
            valence_band_maximum=vbm,
            conduction_band_minimum=cbm,
            electron_effective_mass=electron_mass,
            hole_effective_mass=hole_mass,
            dielectric_constant=dielectric,
            confidence=confidence
        )
        
        # Add uncertainty bounds
        properties.add_uncertainty_bounds()
        
        # Update structure with formation energy
        structure.formation_energy = formation_energy
        
        logger.info(f"Predicted bandgap: {bandgap:.2f} eV, efficiency: {properties.predicted_efficiency:.1f}%")
        return properties
    
    async def predict_formation_energy(self, structure: PerovskiteStructure) -> float:
        """Predict formation energy for a structure"""
        formation_energy, _ = self.models["formation_energy"](structure)
        return formation_energy
    
    async def predict_decomposition_energy(self, structure: PerovskiteStructure) -> float:
        """Predict decomposition energy for a structure"""
        # Simplified decomposition energy calculation
        formation_energy = await self.predict_formation_energy(structure)
        
        # Decomposition energy is typically higher than formation energy
        decomposition_energy = abs(formation_energy) + 0.3 + np.random.normal(0, 0.1)
        
        return decomposition_energy
    
    async def generate_candidates(self, 
                                base_composition: str,
                                strategy: str = "cation_substitution",
                                n_candidates: int = 50) -> List[str]:
        """Generate candidate compositions using ML-guided design"""
        logger.info(f"Generating {n_candidates} candidates from {base_composition} using {strategy}")
        
        candidates = []
        
        if strategy == "cation_substitution":
            # Generate cation substitution candidates
            cations = ["MA", "FA", "Cs", "Rb", "K"]
            anions = ["I", "Br", "Cl"]
            
            for _ in range(n_candidates):
                # Random cation selection
                cation = np.random.choice(cations)
                
                # Random anion selection (with bias towards I)
                anion = np.random.choice(anions, p=[0.7, 0.2, 0.1])
                
                # Create composition
                composition = f"{cation}Pb{anion}3"
                
                # Add some mixed compositions
                if np.random.random() < 0.3:
                    cation2 = np.random.choice([c for c in cations if c != cation])
                    ratio = np.random.uniform(0.1, 0.9)
                    composition = f"{cation}{ratio:.1f}{cation2}{1-ratio:.1f}Pb{anion}3"
                
                candidates.append(composition)
        
        elif strategy == "anion_substitution":
            # Generate anion substitution candidates
            base_cation = base_composition.split("Pb")[0]
            anions = ["I", "Br", "Cl"]
            
            for _ in range(n_candidates):
                # Random anion mixing
                anion1 = np.random.choice(anions)
                anion2 = np.random.choice([a for a in anions if a != anion1])
                ratio = np.random.uniform(0.1, 0.9)
                
                composition = f"{base_cation}Pb{anion1}{ratio*3:.1f}{anion2}{(1-ratio)*3:.1f}"
                candidates.append(composition)
        
        elif strategy == "mixed_composition":
            # Generate mixed cation/anion compositions
            cations = ["MA", "FA", "Cs"]
            anions = ["I", "Br", "Cl"]
            
            for _ in range(n_candidates):
                # Random cation mixing
                cation1 = np.random.choice(cations)
                cation2 = np.random.choice([c for c in cations if c != cation1])
                cation_ratio = np.random.uniform(0.2, 0.8)
                
                # Random anion mixing
                anion1 = np.random.choice(anions)
                anion2 = np.random.choice([a for a in anions if a != anion1])
                anion_ratio = np.random.uniform(0.2, 0.8)
                
                composition = (f"{cation1}{cation_ratio:.1f}{cation2}{1-cation_ratio:.1f}"
                             f"Pb{anion1}{anion_ratio*3:.1f}{anion2}{(1-anion_ratio)*3:.1f}")
                candidates.append(composition)
        
        # Remove duplicates and invalid compositions
        candidates = list(set(candidates))
        valid_candidates = []
        
        for comp in candidates:
            try:
                # Validate composition by trying to create structure
                PerovskiteStructure.from_composition(comp)
                valid_candidates.append(comp)
            except:
                continue
        
        logger.info(f"Generated {len(valid_candidates)} valid candidates")
        return valid_candidates[:n_candidates]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "models": list(self.models.keys()),
            "versions": self.model_versions,
            "training_data_size": {k: len(v) for k, v in self.training_data.items()},
            "last_updated": datetime.now().isoformat()
        }
    
    def update_model(self, model_name: str, training_data: List[Dict[str, Any]]):
        """Update model with new training data"""
        logger.info(f"Updating {model_name} model with {len(training_data)} samples")
        
        # Store training data
        self.training_data[model_name] = training_data
        
        # In a real implementation, this would retrain the model
        # For now, we just update the version
        current_version = self.model_versions.get(model_name, "v1.0")
        version_parts = current_version.split(".")
        new_minor = int(version_parts[1]) + 1
        self.model_versions[model_name] = f"v{version_parts[0][1:]}.{new_minor}"
        
        logger.info(f"Updated {model_name} to version {self.model_versions[model_name]}")
    
    def validate_predictions(self, 
                           test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Validate model predictions against test data"""
        logger.info(f"Validating predictions on {len(test_data)} test samples")
        
        validation_results = {}
        
        for model_name in self.models.keys():
            if model_name in ["bandgap", "formation_energy", "stability", "efficiency"]:
                errors = []
                
                for sample in test_data:
                    if model_name in sample:
                        # Create structure from sample
                        structure = PerovskiteStructure.from_composition(sample["composition"])
                        
                        # Get prediction
                        if model_name == "bandgap":
                            pred, _ = self.models[model_name](structure)
                        elif model_name == "formation_energy":
                            pred, _ = self.models[model_name](structure)
                        elif model_name == "stability":
                            pred, _ = self.models[model_name](structure)
                        elif model_name == "efficiency":
                            pred, _ = self.models[model_name](structure)
                        
                        # Calculate error
                        actual = sample[model_name]
                        error = abs(pred - actual) / actual
                        errors.append(error)
                
                if errors:
                    validation_results[model_name] = {
                        "mean_absolute_error": np.mean(errors),
                        "std_error": np.std(errors),
                        "n_samples": len(errors)
                    }
        
        logger.info(f"Validation complete: {validation_results}")
        return validation_results
    
    def __repr__(self) -> str:
        return f"PropertyPredictor(models={list(self.models.keys())})"