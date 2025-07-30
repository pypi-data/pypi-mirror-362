from typing import Dict, List, Optional, Any
import asyncio
import logging
from dataclasses import dataclass
from agents import Agent, Runner
from openai import OpenAI

from ..models.crystal_structure import PerovskiteStructure
from ..models.electronic_properties import ElectronicProperties
from ..ml.property_prediction import PropertyPredictor
from ..database.crud import MaterialsCRUD
from ..utils.exceptions import DiscoveryError
from ..utils.validators import validate_composition

logger = logging.getLogger(__name__)

@dataclass
class DiscoveryResult:
    """Results from materials discovery process"""
    composition: str
    structure: PerovskiteStructure
    predicted_properties: ElectronicProperties
    confidence: float
    synthesis_feasibility: float
    cost_estimate: float
    
class MaterialsDiscoveryAgent(Agent):
    """AI agent for autonomous perovskite materials discovery"""
    
    def __init__(self, 
                 predictor: PropertyPredictor,
                 database: MaterialsCRUD,
                 target_properties: Optional[Dict[str, float]] = None):
        super().__init__(
            name="MaterialsDiscoveryAgent",
            instructions="""
            You are an expert materials scientist specializing in perovskite solar cells.
            Your role is to:
            1. Generate novel perovskite compositions using AI-guided design
            2. Predict material properties using machine learning models
            3. Evaluate synthesis feasibility and cost-effectiveness
            4. Coordinate with synthesis and characterization agents
            5. Optimize compositions for target device performance
            
            Key capabilities:
            - Crystal structure prediction and analysis
            - Electronic property prediction (bandgap, carrier mobility)
            - Stability analysis (formation energy, decomposition)
            - Defect chemistry understanding
            - Synthesis route planning
            
            Always provide scientific rationale for your recommendations.
            """,
            model="gpt-4o",
            tools=[
                self.generate_composition,
                self.predict_properties,
                self.evaluate_stability,
                self.estimate_synthesis_cost,
                self.search_literature
            ]
        )
        
        self.predictor = predictor
        self.database = database
        self.target_properties = target_properties or {
            'bandgap': 1.3,  # eV
            'efficiency': 25.0,  # %
            'stability': 1000.0,  # hours
        }
        
    async def generate_composition(self, 
                                 base_composition: str = "MAPbI3",
                                 modification_strategy: str = "cation_substitution") -> List[str]:
        """Generate novel perovskite compositions using AI-guided design"""
        try:
            # Validate input composition
            validate_composition(base_composition)
            
            # Use ML model to generate candidates
            candidates = await self.predictor.generate_candidates(
                base_composition=base_composition,
                strategy=modification_strategy,
                n_candidates=50
            )
            
            # Filter candidates based on stability and feasibility
            filtered_candidates = []
            for candidate in candidates:
                stability_score = await self.evaluate_stability(candidate)
                if stability_score > 0.7:  # Stable compositions only
                    filtered_candidates.append(candidate)
            
            logger.info(f"Generated {len(filtered_candidates)} stable candidates from {base_composition}")
            return filtered_candidates[:10]  # Return top 10
            
        except Exception as e:
            logger.error(f"Error generating compositions: {e}")
            raise DiscoveryError(f"Composition generation failed: {e}")
    
    async def predict_properties(self, composition: str) -> ElectronicProperties:
        """Predict electronic and optical properties using ML models"""
        try:
            # Create crystal structure
            structure = PerovskiteStructure.from_composition(composition)
            
            # Predict properties using trained models
            properties = await self.predictor.predict_properties(structure)
            
            # Add uncertainty quantification
            properties.add_uncertainty_bounds()
            
            return properties
            
        except Exception as e:
            logger.error(f"Error predicting properties for {composition}: {e}")
            raise DiscoveryError(f"Property prediction failed: {e}")
    
    async def evaluate_stability(self, composition: str) -> float:
        """Evaluate thermodynamic and kinetic stability"""
        try:
            structure = PerovskiteStructure.from_composition(composition)
            
            # Calculate formation energy
            formation_energy = await self.predictor.predict_formation_energy(structure)
            
            # Calculate decomposition energy
            decomposition_energy = await self.predictor.predict_decomposition_energy(structure)
            
            # Calculate stability score (0-1)
            stability_score = max(0, min(1, (decomposition_energy - formation_energy) / 2.0))
            
            return stability_score
            
        except Exception as e:
            logger.error(f"Error evaluating stability for {composition}: {e}")
            return 0.0
    
    async def estimate_synthesis_cost(self, composition: str) -> Dict[str, float]:
        """Estimate synthesis cost and scalability"""
        try:
            # Parse composition to extract precursors
            precursors = PerovskiteStructure.parse_precursors(composition)
            
            # Calculate cost based on precursor prices and quantities
            total_cost = 0.0
            cost_breakdown = {}
            
            for precursor, amount in precursors.items():
                unit_cost = await self.database.get_precursor_cost(precursor)
                precursor_cost = unit_cost * amount
                cost_breakdown[precursor] = precursor_cost
                total_cost += precursor_cost
            
            return {
                'total_cost_per_gram': total_cost,
                'breakdown': cost_breakdown,
                'scalability_factor': min(1.0, 100.0 / total_cost)  # Higher for cheaper materials
            }
            
        except Exception as e:
            logger.error(f"Error estimating synthesis cost for {composition}: {e}")
            return {'total_cost_per_gram': float('inf'), 'breakdown': {}, 'scalability_factor': 0.0}
    
    async def search_literature(self, composition: str) -> List[Dict[str, Any]]:
        """Search scientific literature for relevant studies"""
        try:
            # Search Materials Project database
            mp_results = await self.database.search_materials_project(composition)
            
            # Search scientific publications
            pub_results = await self.database.search_publications(composition)
            
            # Combine and rank results
            all_results = mp_results + pub_results
            ranked_results = sorted(all_results, key=lambda x: x.get('relevance', 0), reverse=True)
            
            return ranked_results[:5]  # Return top 5 most relevant
            
        except Exception as e:
            logger.error(f"Error searching literature for {composition}: {e}")
            return []
    
    async def discover_materials(self, 
                               target_properties: Optional[Dict[str, float]] = None,
                               max_candidates: int = 10) -> List[DiscoveryResult]:
        """Main discovery workflow"""
        try:
            if target_properties:
                self.target_properties.update(target_properties)
            
            # Generate candidate compositions
            candidates = await self.generate_composition()
            
            # Evaluate each candidate
            results = []
            for composition in candidates:
                try:
                    # Predict properties
                    properties = await self.predict_properties(composition)
                    
                    # Evaluate stability
                    stability = await self.evaluate_stability(composition)
                    
                    # Estimate cost
                    cost_data = await self.estimate_synthesis_cost(composition)
                    
                    # Calculate overall score
                    score = self._calculate_discovery_score(
                        properties, stability, cost_data['scalability_factor']
                    )
                    
                    result = DiscoveryResult(
                        composition=composition,
                        structure=PerovskiteStructure.from_composition(composition),
                        predicted_properties=properties,
                        confidence=score,
                        synthesis_feasibility=stability,
                        cost_estimate=cost_data['total_cost_per_gram']
                    )
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.warning(f"Failed to evaluate {composition}: {e}")
                    continue
            
            # Sort by confidence score
            results.sort(key=lambda x: x.confidence, reverse=True)
            
            return results[:max_candidates]
            
        except Exception as e:
            logger.error(f"Materials discovery failed: {e}")
            raise DiscoveryError(f"Discovery workflow failed: {e}")
    
    def _calculate_discovery_score(self, 
                                 properties: ElectronicProperties,
                                 stability: float,
                                 scalability: float) -> float:
        """Calculate overall discovery score"""
        # Weight factors
        w_efficiency = 0.4
        w_stability = 0.3
        w_cost = 0.2
        w_feasibility = 0.1
        
        # Normalize property scores
        efficiency_score = min(1.0, properties.predicted_efficiency / self.target_properties['efficiency'])
        stability_score = stability
        cost_score = scalability
        feasibility_score = properties.confidence
        
        total_score = (
            w_efficiency * efficiency_score +
            w_stability * stability_score +
            w_cost * cost_score +
            w_feasibility * feasibility_score
        )
        
        return total_score
    
    def handoff_to_synthesis(self, discovery_results: List[DiscoveryResult]):
        """Hand off promising candidates to synthesis agent"""
        # Select top candidates for synthesis
        top_candidates = discovery_results[:3]
        
        synthesis_request = {
            'candidates': [
                {
                    'composition': result.composition,
                    'predicted_properties': result.predicted_properties.model_dump(),
                    'priority': result.confidence
                }
                for result in top_candidates
            ],
            'synthesis_conditions': {
                'temperature_range': (100, 200),  # °C
                'atmosphere': 'nitrogen',
                'annealing_time': 60  # minutes
            }
        }
        
        return self.handoff(
            "SynthesisAgent",
            synthesis_request=synthesis_request,
            context="High-priority materials from discovery phase"
        )
    
    def handoff_to_characterization(self, materials_batch: List[Dict]):
        """Hand off synthesized materials to characterization agent"""
        characterization_request = {
            'materials': materials_batch,
            'priority_tests': [
                'xrd_structure',
                'uv_vis_bandgap',
                'plqy_efficiency',
                'stability_testing'
            ],
            'expected_timeline': '48_hours'
        }
        
        return self.handoff(
            "CharacterizationAgent",
            characterization_request=characterization_request,
            context="Materials from synthesis phase requiring characterization"
        )