"""
Characterization suite for perovskite materials.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class CharacterizationResult:
    """Result from a characterization measurement"""
    measurement_type: str
    sample_id: str
    measured_value: float
    unit: str
    uncertainty: Optional[float] = None
    measurement_conditions: Optional[Dict[str, Any]] = None
    raw_data: Optional[Dict[str, Any]] = None
    quality_score: float = 1.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class XRDResult:
    """X-ray diffraction results"""
    phases: List[str]
    crystallinity: float
    grain_size: float
    lattice_parameters: Dict[str, float]
    peak_positions: List[float]
    peak_intensities: List[float]
    preferred_orientation: Optional[str] = None

@dataclass
class UVVisResult:
    """UV-Vis spectroscopy results"""
    wavelengths: List[float]
    absorbance: List[float]
    transmittance: List[float]
    bandgap: float
    urbach_energy: float
    absorption_coefficient: List[float]

@dataclass
class PLQYResult:
    """Photoluminescence quantum yield results"""
    quantum_yield: float
    lifetime: float
    peak_wavelength: float
    fwhm: float
    emission_spectrum: Dict[str, List[float]]

@dataclass
class SEMResult:
    """Scanning electron microscopy results"""
    morphology_description: str
    grain_size_distribution: List[float]
    surface_roughness: float
    coverage: float
    defect_density: float
    image_paths: List[str]

class CharacterizationSuite:
    """Comprehensive characterization suite for perovskite materials"""
    
    def __init__(self):
        self.available_techniques = [
            "xrd", "uv_vis", "plqy", "sem", "afm", "xps", 
            "ftir", "raman", "pds", "trpl", "impedance"
        ]
        self.calibration_data = {}
        self._load_calibration_data()
    
    def _load_calibration_data(self):
        """Load calibration data for instruments"""
        # Placeholder calibration data
        self.calibration_data = {
            "xrd": {"wavelength": 1.5406, "calibration_factor": 1.0},
            "uv_vis": {"baseline_correction": True, "integration_time": 100},
            "plqy": {"excitation_wavelength": 450, "reference_qy": 0.95},
            "sem": {"acceleration_voltage": 5000, "working_distance": 10},
        }
    
    async def run_xrd(self, sample_id: str, composition: str) -> XRDResult:
        """Run X-ray diffraction analysis"""
        logger.info(f"Running XRD analysis for sample {sample_id}")
        
        # Simulate XRD measurement
        # In reality, this would interface with actual XRD equipment
        
        # Generate realistic XRD data based on composition
        if "MAPbI3" in composition:
            phases = ["MAPbI3_tetragonal", "PbI2_trace"]
            crystallinity = 0.85 + np.random.normal(0, 0.05)
            grain_size = 150 + np.random.normal(0, 20)  # nm
            lattice_params = {"a": 8.855, "b": 8.855, "c": 12.659}
            peak_positions = [14.2, 28.5, 31.9, 40.7, 43.2]
            peak_intensities = [100, 60, 45, 30, 25]
            
        elif "FAPbI3" in composition:
            phases = ["FAPbI3_cubic", "PbI2_trace"]
            crystallinity = 0.80 + np.random.normal(0, 0.05)
            grain_size = 200 + np.random.normal(0, 30)  # nm
            lattice_params = {"a": 6.362, "b": 6.362, "c": 6.362}
            peak_positions = [13.9, 27.8, 31.5, 40.2, 42.8]
            peak_intensities = [100, 55, 40, 28, 22]
            
        else:
            # Generic perovskite
            phases = [f"{composition}_cubic"]
            crystallinity = 0.75 + np.random.normal(0, 0.08)
            grain_size = 120 + np.random.normal(0, 25)
            lattice_params = {"a": 6.0, "b": 6.0, "c": 6.0}
            peak_positions = [14.0, 28.0, 31.0, 40.0, 43.0]
            peak_intensities = [100, 50, 35, 25, 20]
        
        # Add some measurement noise
        crystallinity = max(0.1, min(1.0, crystallinity))
        grain_size = max(10, grain_size)
        
        result = XRDResult(
            phases=phases,
            crystallinity=crystallinity,
            grain_size=grain_size,
            lattice_parameters=lattice_params,
            peak_positions=peak_positions,
            peak_intensities=peak_intensities,
            preferred_orientation="(100)" if crystallinity > 0.8 else None
        )
        
        logger.info(f"XRD analysis complete: crystallinity={crystallinity:.2f}, grain_size={grain_size:.1f}nm")
        return result
    
    async def run_uv_vis(self, sample_id: str, composition: str) -> UVVisResult:
        """Run UV-Vis spectroscopy analysis"""
        logger.info(f"Running UV-Vis analysis for sample {sample_id}")
        
        # Generate wavelength range (nm)
        wavelengths = np.linspace(300, 800, 500).tolist()
        
        # Simulate absorption spectrum based on composition
        if "MAPbI3" in composition:
            bandgap = 1.55 + np.random.normal(0, 0.05)  # eV
            urbach_energy = 15 + np.random.normal(0, 2)  # meV
        elif "FAPbI3" in composition:
            bandgap = 1.48 + np.random.normal(0, 0.05)  # eV
            urbach_energy = 12 + np.random.normal(0, 2)  # meV
        else:
            bandgap = 1.5 + np.random.normal(0, 0.1)  # eV
            urbach_energy = 15 + np.random.normal(0, 3)  # meV
        
        # Convert bandgap to wavelength
        bandgap_wavelength = 1240 / bandgap  # nm
        
        # Generate absorption spectrum
        absorbance = []
        transmittance = []
        absorption_coefficient = []
        
        for wl in wavelengths:
            if wl < bandgap_wavelength:
                # Strong absorption below bandgap
                abs_coeff = 1e5 * np.exp(-(1240/wl - bandgap) / (urbach_energy/1000))
                abs_val = min(3.0, abs_coeff * 500e-9)  # Assuming 500nm film
            else:
                # Weak absorption above bandgap
                abs_coeff = 1e3 * np.exp(-(wl - bandgap_wavelength) / 50)
                abs_val = min(0.1, abs_coeff * 500e-9)
            
            # Add some noise
            abs_val += np.random.normal(0, 0.02)
            abs_val = max(0, abs_val)
            
            absorbance.append(abs_val)
            transmittance.append(10**(-abs_val))
            absorption_coefficient.append(abs_coeff)
        
        result = UVVisResult(
            wavelengths=wavelengths,
            absorbance=absorbance,
            transmittance=transmittance,
            bandgap=bandgap,
            urbach_energy=urbach_energy,
            absorption_coefficient=absorption_coefficient
        )
        
        logger.info(f"UV-Vis analysis complete: bandgap={bandgap:.2f}eV, urbach_energy={urbach_energy:.1f}meV")
        return result
    
    async def run_plqy(self, sample_id: str, composition: str) -> PLQYResult:
        """Run photoluminescence quantum yield measurement"""
        logger.info(f"Running PLQY analysis for sample {sample_id}")
        
        # Simulate PLQY measurement
        if "MAPbI3" in composition:
            base_qy = 0.15
            peak_wl = 780
            lifetime = 150  # ns
        elif "FAPbI3" in composition:
            base_qy = 0.12
            peak_wl = 820
            lifetime = 200  # ns
        else:
            base_qy = 0.10
            peak_wl = 800
            lifetime = 100  # ns
        
        # Add realistic variations
        quantum_yield = base_qy + np.random.normal(0, 0.03)
        quantum_yield = max(0.01, min(1.0, quantum_yield))
        
        lifetime = lifetime + np.random.normal(0, 20)
        lifetime = max(10, lifetime)
        
        peak_wavelength = peak_wl + np.random.normal(0, 10)
        fwhm = 40 + np.random.normal(0, 5)
        
        # Generate emission spectrum
        wavelengths = np.linspace(peak_wavelength - 100, peak_wavelength + 100, 200)
        intensities = np.exp(-0.5 * ((wavelengths - peak_wavelength) / (fwhm/2.35))**2)
        
        # Normalize and add noise
        intensities = intensities / np.max(intensities) * quantum_yield
        intensities += np.random.normal(0, 0.01, len(intensities))
        intensities = np.maximum(0, intensities)
        
        emission_spectrum = {
            "wavelengths": wavelengths.tolist(),
            "intensities": intensities.tolist()
        }
        
        result = PLQYResult(
            quantum_yield=quantum_yield,
            lifetime=lifetime,
            peak_wavelength=peak_wavelength,
            fwhm=fwhm,
            emission_spectrum=emission_spectrum
        )
        
        logger.info(f"PLQY analysis complete: QY={quantum_yield:.3f}, lifetime={lifetime:.1f}ns")
        return result
    
    async def run_sem(self, sample_id: str, composition: str) -> SEMResult:
        """Run scanning electron microscopy analysis"""
        logger.info(f"Running SEM analysis for sample {sample_id}")
        
        # Simulate SEM measurement
        if "MAPbI3" in composition:
            base_grain_size = 200
            surface_roughness = 15
            coverage = 0.95
            defect_density = 1e8  # cm^-2
            morphology = "cubic grains with some pinholes"
        elif "FAPbI3" in composition:
            base_grain_size = 300
            surface_roughness = 20
            coverage = 0.92
            defect_density = 5e7  # cm^-2
            morphology = "large cubic grains with good connectivity"
        else:
            base_grain_size = 150
            surface_roughness = 25
            coverage = 0.88
            defect_density = 2e8  # cm^-2
            morphology = "irregular grains with moderate coverage"
        
        # Generate grain size distribution
        grain_sizes = np.random.lognormal(
            np.log(base_grain_size), 0.3, 100
        ).tolist()
        
        # Add variations
        surface_roughness += np.random.normal(0, 3)
        coverage += np.random.normal(0, 0.05)
        defect_density *= (1 + np.random.normal(0, 0.2))
        
        # Clamp values
        surface_roughness = max(1, surface_roughness)
        coverage = max(0.1, min(1.0, coverage))
        defect_density = max(1e6, defect_density)
        
        result = SEMResult(
            morphology_description=morphology,
            grain_size_distribution=grain_sizes,
            surface_roughness=surface_roughness,
            coverage=coverage,
            defect_density=defect_density,
            image_paths=[f"sem_{sample_id}_top.tif", f"sem_{sample_id}_cross.tif"]
        )
        
        logger.info(f"SEM analysis complete: avg_grain_size={np.mean(grain_sizes):.1f}nm, coverage={coverage:.2f}")
        return result
    
    async def run_comprehensive_characterization(self, 
                                               sample_id: str, 
                                               composition: str,
                                               techniques: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run comprehensive characterization suite"""
        if techniques is None:
            techniques = ["xrd", "uv_vis", "plqy", "sem"]
        
        logger.info(f"Running comprehensive characterization for sample {sample_id}")
        
        results = {}
        
        # Run each requested technique
        for technique in techniques:
            try:
                if technique == "xrd":
                    results["xrd"] = await self.run_xrd(sample_id, composition)
                elif technique == "uv_vis":
                    results["uv_vis"] = await self.run_uv_vis(sample_id, composition)
                elif technique == "plqy":
                    results["plqy"] = await self.run_plqy(sample_id, composition)
                elif technique == "sem":
                    results["sem"] = await self.run_sem(sample_id, composition)
                else:
                    logger.warning(f"Technique {technique} not implemented")
                    
            except Exception as e:
                logger.error(f"Error running {technique} for sample {sample_id}: {e}")
                results[technique] = {"error": str(e)}
        
        # Calculate overall quality score
        quality_scores = []
        if "xrd" in results and hasattr(results["xrd"], "crystallinity"):
            quality_scores.append(results["xrd"].crystallinity)
        if "plqy" in results and hasattr(results["plqy"], "quantum_yield"):
            quality_scores.append(results["plqy"].quantum_yield * 10)  # Scale to 0-1
        if "sem" in results and hasattr(results["sem"], "coverage"):
            quality_scores.append(results["sem"].coverage)
        
        overall_quality = np.mean(quality_scores) if quality_scores else 0.5
        
        results["summary"] = {
            "sample_id": sample_id,
            "composition": composition,
            "techniques_used": techniques,
            "overall_quality_score": overall_quality,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Comprehensive characterization complete: quality_score={overall_quality:.2f}")
        return results
    
    def get_available_techniques(self) -> List[str]:
        """Get list of available characterization techniques"""
        return self.available_techniques.copy()
    
    def export_results(self, results: Dict[str, Any], format: str = "json") -> str:
        """Export characterization results"""
        if format == "json":
            return json.dumps(results, indent=2, default=str)
        elif format == "yaml":
            import yaml
            return yaml.dump(results, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def validate_sample_quality(self, results: Dict[str, Any]) -> Dict[str, bool]:
        """Validate sample quality based on characterization results"""
        validation = {}
        
        # XRD validation
        if "xrd" in results:
            xrd = results["xrd"]
            validation["crystallinity_ok"] = xrd.crystallinity > 0.7
            validation["phase_purity_ok"] = len(xrd.phases) <= 2
            validation["grain_size_ok"] = xrd.grain_size > 50  # nm
        
        # UV-Vis validation
        if "uv_vis" in results:
            uv_vis = results["uv_vis"]
            validation["bandgap_ok"] = 1.0 <= uv_vis.bandgap <= 2.0
            validation["urbach_energy_ok"] = uv_vis.urbach_energy < 20  # meV
        
        # PLQY validation
        if "plqy" in results:
            plqy = results["plqy"]
            validation["quantum_yield_ok"] = plqy.quantum_yield > 0.05
            validation["lifetime_ok"] = plqy.lifetime > 50  # ns
        
        # SEM validation
        if "sem" in results:
            sem = results["sem"]
            validation["coverage_ok"] = sem.coverage > 0.8
            validation["defect_density_ok"] = sem.defect_density < 1e9  # cm^-2
        
        return validation
    
    def __repr__(self) -> str:
        return f"CharacterizationSuite(techniques={len(self.available_techniques)})"