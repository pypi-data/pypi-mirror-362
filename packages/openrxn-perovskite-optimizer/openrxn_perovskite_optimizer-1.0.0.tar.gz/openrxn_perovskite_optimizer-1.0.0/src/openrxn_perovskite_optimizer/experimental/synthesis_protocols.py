"""
Synthesis protocols for perovskite materials.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class SynthesisStep:
    """Individual step in a synthesis protocol"""
    step_name: str
    description: str
    temperature: float  # °C
    time: float  # minutes
    atmosphere: str
    equipment: List[str]
    precautions: List[str]
    expected_outcome: str

@dataclass
class SynthesisConditions:
    """Synthesis conditions and parameters"""
    temperature: float
    pressure: float
    atmosphere: str
    humidity: float
    stirring_speed: Optional[float] = None
    annealing_time: Optional[float] = None
    cooling_rate: Optional[float] = None

class SynthesisProtocol:
    """Complete synthesis protocol for perovskite materials"""
    
    def __init__(self):
        self.protocols = {}
        self._load_standard_protocols()
    
    def _load_standard_protocols(self):
        """Load standard synthesis protocols"""
        # Solution processing protocol for MAPbI3
        self.protocols["MAPbI3_solution"] = {
            "composition": "MAPbI3",
            "method": "solution_processing",
            "precursors": {
                "PbI2": 1.0,
                "MAI": 0.5,
                "DMF": 1.0,
                "DMSO": 0.1
            },
            "steps": [
                SynthesisStep(
                    step_name="precursor_dissolution",
                    description="Dissolve PbI2 and MAI in DMF:DMSO",
                    temperature=60,
                    time=30,
                    atmosphere="nitrogen",
                    equipment=["magnetic_stirrer", "hotplate"],
                    precautions=["wear_gloves", "use_fume_hood"],
                    expected_outcome="clear_solution"
                ),
                SynthesisStep(
                    step_name="film_deposition",
                    description="Spin coat solution on substrate",
                    temperature=25,
                    time=1,
                    atmosphere="nitrogen",
                    equipment=["spin_coater"],
                    precautions=["clean_substrate", "controlled_humidity"],
                    expected_outcome="uniform_film"
                ),
                SynthesisStep(
                    step_name="annealing",
                    description="Anneal film to crystallize perovskite",
                    temperature=100,
                    time=10,
                    atmosphere="nitrogen",
                    equipment=["hotplate", "nitrogen_flow"],
                    precautions=["gradual_heating", "monitor_color_change"],
                    expected_outcome="dark_brown_film"
                )
            ],
            "conditions": SynthesisConditions(
                temperature=100,
                pressure=1.0,
                atmosphere="nitrogen",
                humidity=0.1,
                stirring_speed=500,
                annealing_time=10,
                cooling_rate=5
            ),
            "estimated_duration": 2.0,  # hours
            "estimated_cost": 15.0,  # USD
            "success_rate": 0.85,
            "yield_percentage": 90.0
        }
        
        # Add FAPbI3 protocol
        self.protocols["FAPbI3_solution"] = {
            "composition": "FAPbI3",
            "method": "solution_processing",
            "precursors": {
                "PbI2": 1.0,
                "FAI": 0.5,
                "DMF": 0.8,
                "DMSO": 0.2
            },
            "steps": [
                SynthesisStep(
                    step_name="precursor_dissolution",
                    description="Dissolve PbI2 and FAI in DMF:DMSO",
                    temperature=70,
                    time=45,
                    atmosphere="nitrogen",
                    equipment=["magnetic_stirrer", "hotplate"],
                    precautions=["wear_gloves", "use_fume_hood"],
                    expected_outcome="clear_solution"
                ),
                SynthesisStep(
                    step_name="film_deposition",
                    description="Spin coat with anti-solvent treatment",
                    temperature=25,
                    time=1,
                    atmosphere="nitrogen",
                    equipment=["spin_coater"],
                    precautions=["toluene_dripping", "controlled_humidity"],
                    expected_outcome="uniform_film"
                ),
                SynthesisStep(
                    step_name="annealing",
                    description="Two-step annealing process",
                    temperature=150,
                    time=15,
                    atmosphere="nitrogen",
                    equipment=["hotplate", "nitrogen_flow"],
                    precautions=["gradual_heating", "monitor_phase_transition"],
                    expected_outcome="black_film"
                )
            ],
            "conditions": SynthesisConditions(
                temperature=150,
                pressure=1.0,
                atmosphere="nitrogen",
                humidity=0.05,
                stirring_speed=600,
                annealing_time=15,
                cooling_rate=3
            ),
            "estimated_duration": 3.0,  # hours
            "estimated_cost": 20.0,  # USD
            "success_rate": 0.75,
            "yield_percentage": 85.0
        }
    
    async def get_protocol(self, composition: str, method: str = "solution_processing") -> Dict[str, Any]:
        """Get synthesis protocol for a composition"""
        protocol_key = f"{composition}_{method}"
        
        if protocol_key in self.protocols:
            return self.protocols[protocol_key]
        
        # Generate protocol if not found
        return await self._generate_protocol(composition, method)
    
    async def _generate_protocol(self, composition: str, method: str) -> Dict[str, Any]:
        """Generate a new synthesis protocol"""
        logger.info(f"Generating protocol for {composition} using {method}")
        
        # Basic protocol template
        protocol = {
            "composition": composition,
            "method": method,
            "precursors": self._determine_precursors(composition),
            "steps": self._generate_steps(composition, method),
            "conditions": self._determine_conditions(composition, method),
            "estimated_duration": 2.5,
            "estimated_cost": 18.0,
            "success_rate": 0.7,
            "yield_percentage": 80.0
        }
        
        # Cache the generated protocol
        self.protocols[f"{composition}_{method}"] = protocol
        
        return protocol
    
    def _determine_precursors(self, composition: str) -> Dict[str, float]:
        """Determine precursors for a composition"""
        # Simple parsing - in reality would use more sophisticated chemistry
        if "Pb" in composition and "I" in composition:
            precursors = {"PbI2": 1.0}
            
            if "MA" in composition:
                precursors["MAI"] = 0.5
            elif "FA" in composition:
                precursors["FAI"] = 0.5
            elif "Cs" in composition:
                precursors["CsI"] = 0.5
            
            # Add solvents
            precursors.update({
                "DMF": 1.0,
                "DMSO": 0.1
            })
            
        return precursors
    
    def _generate_steps(self, composition: str, method: str) -> List[SynthesisStep]:
        """Generate synthesis steps"""
        if method == "solution_processing":
            return [
                SynthesisStep(
                    step_name="precursor_dissolution",
                    description=f"Dissolve precursors for {composition}",
                    temperature=65,
                    time=35,
                    atmosphere="nitrogen",
                    equipment=["magnetic_stirrer", "hotplate"],
                    precautions=["wear_gloves", "use_fume_hood"],
                    expected_outcome="clear_solution"
                ),
                SynthesisStep(
                    step_name="film_deposition",
                    description="Deposit film via spin coating",
                    temperature=25,
                    time=1,
                    atmosphere="nitrogen",
                    equipment=["spin_coater"],
                    precautions=["clean_substrate", "controlled_humidity"],
                    expected_outcome="uniform_film"
                ),
                SynthesisStep(
                    step_name="annealing",
                    description="Crystallize perovskite phase",
                    temperature=120,
                    time=12,
                    atmosphere="nitrogen",
                    equipment=["hotplate", "nitrogen_flow"],
                    precautions=["gradual_heating", "monitor_color_change"],
                    expected_outcome="crystalline_film"
                )
            ]
        
        return []
    
    def _determine_conditions(self, composition: str, method: str) -> SynthesisConditions:
        """Determine synthesis conditions"""
        # Default conditions
        return SynthesisConditions(
            temperature=120,
            pressure=1.0,
            atmosphere="nitrogen",
            humidity=0.1,
            stirring_speed=500,
            annealing_time=12,
            cooling_rate=5
        )
    
    def estimate_time(self, composition: str, method: str = "solution_processing") -> float:
        """Estimate synthesis time in hours"""
        protocol_key = f"{composition}_{method}"
        if protocol_key in self.protocols:
            return self.protocols[protocol_key]["estimated_duration"]
        return 2.5  # Default estimate
    
    def estimate_cost(self, composition: str, method: str = "solution_processing") -> float:
        """Estimate synthesis cost in USD"""
        protocol_key = f"{composition}_{method}"
        if protocol_key in self.protocols:
            return self.protocols[protocol_key]["estimated_cost"]
        return 18.0  # Default estimate
    
    def get_success_rate(self, composition: str, method: str = "solution_processing") -> float:
        """Get expected success rate"""
        protocol_key = f"{composition}_{method}"
        if protocol_key in self.protocols:
            return self.protocols[protocol_key]["success_rate"]
        return 0.7  # Default estimate
    
    def export_protocol(self, composition: str, method: str = "solution_processing", 
                       format: str = "json") -> str:
        """Export protocol in specified format"""
        protocol_key = f"{composition}_{method}"
        if protocol_key not in self.protocols:
            raise ValueError(f"Protocol not found: {protocol_key}")
        
        protocol = self.protocols[protocol_key]
        
        if format == "json":
            return json.dumps(protocol, indent=2, default=str)
        elif format == "yaml":
            import yaml
            return yaml.dump(protocol, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def list_protocols(self) -> List[str]:
        """List available protocols"""
        return list(self.protocols.keys())
    
    def __repr__(self) -> str:
        return f"SynthesisProtocol(protocols={len(self.protocols)})"