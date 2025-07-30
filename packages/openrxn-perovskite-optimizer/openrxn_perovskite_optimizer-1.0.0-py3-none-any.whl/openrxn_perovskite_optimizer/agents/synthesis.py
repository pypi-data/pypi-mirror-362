from typing import Dict, List, Optional, Any
import asyncio
import logging
from dataclasses import dataclass
from agents import Agent
from datetime import datetime, timedelta

from ..experimental.synthesis_protocols import SynthesisProtocol
from ..models.crystal_structure import PerovskiteStructure
from ..utils.exceptions import SynthesisError
from ..database.crud import ExperimentalCRUD

logger = logging.getLogger(__name__)

@dataclass
class SynthesisResult:
    """Results from synthesis process"""
    composition: str
    synthesis_method: str
    conditions: Dict[str, Any]
    yield_percentage: float
    purity: float
    batch_id: str
    timestamp: datetime
    quality_metrics: Dict[str, float]

class SynthesisAgent(Agent):
    """AI agent for autonomous perovskite synthesis planning and execution"""
    
    def __init__(self, 
                 protocol_library: SynthesisProtocol,
                 experimental_db: ExperimentalCRUD):
        super().__init__(
            name="SynthesisAgent",
            instructions="""
            You are an expert synthetic chemist specializing in perovskite materials.
            Your role is to:
            1. Design optimal synthesis protocols for perovskite compositions
            2. Optimize reaction conditions for maximum yield and purity
            3. Plan precursor preparation and purification steps
            4. Monitor synthesis progress and adjust parameters
            5. Ensure safety protocols and waste management
            
            Key expertise:
            - Solution processing methods (spin coating, blade coating)
            - Vapor deposition techniques (thermal evaporation, CVD)
            - Solid-state synthesis approaches
            - Crystallization control and nucleation
            - Defect engineering and passivation
            
            Always prioritize safety and reproducibility in your protocols.
            """,
            model="gpt-4o",
            tools=[
                self.design_synthesis_protocol,
                self.optimize_conditions,
                self.plan_precursor_preparation,
                self.monitor_synthesis,
                self.analyze_batch_quality
            ]
        )
        
        self.protocol_library = protocol_library
        self.experimental_db = experimental_db
        
    async def design_synthesis_protocol(self, 
                                      composition: str,
                                      target_properties: Dict[str, float],
                                      synthesis_method: str = "solution_processing") -> Dict[str, Any]:
        """Design optimal synthesis protocol for given composition"""
        try:
            # Parse composition and determine precursors
            structure = PerovskiteStructure.from_composition(composition)
            precursors = structure.get_precursors()
            
            # Select optimal synthesis method
            if synthesis_method == "auto":
                synthesis_method = self._select_optimal_method(composition, target_properties)
            
            # Generate protocol based on method
            if synthesis_method == "solution_processing":
                protocol = await self._design_solution_protocol(precursors, target_properties)
            elif synthesis_method == "vapor_deposition":
                protocol = await self._design_vapor_protocol(precursors, target_properties)
            else:
                protocol = await self._design_solid_state_protocol(precursors, target_properties)
            
            # Add safety considerations
            protocol['safety_measures'] = await self._generate_safety_protocol(precursors)
            
            # Estimate timeline and resources
            protocol['estimated_duration'] = self._estimate_synthesis_time(protocol)
            protocol['required_equipment'] = self._list_required_equipment(protocol)
            
            return protocol
            
        except Exception as e:
            logger.error(f"Error designing synthesis protocol for {composition}: {e}")
            raise SynthesisError(f"Protocol design failed: {e}")
    
    async def _design_solution_protocol(self, 
                                      precursors: Dict[str, float],
                                      target_properties: Dict[str, float]) -> Dict[str, Any]:
        """Design solution-based synthesis protocol"""
        # Determine optimal solvent system
        solvent_system = await self._select_solvent_system(precursors)
        
        # Calculate precursor concentrations
        concentrations = await self._calculate_concentrations(precursors, solvent_system)
        
        # Design crystallization conditions
        crystallization = await self._design_crystallization_conditions(target_properties)
        
        protocol = {
            'method': 'solution_processing',
            'precursors': precursors,
            'solvent_system': solvent_system,
            'concentrations': concentrations,
            'preparation_steps': [
                {
                    'step': 'precursor_dissolution',
                    'temperature': 60,  # °C
                    'time': 30,  # minutes
                    'stirring_speed': 500,  # rpm
                    'atmosphere': 'nitrogen'
                },
                {
                    'step': 'solution_mixing',
                    'temperature': 25,  # °C
                    'time': 15,  # minutes
                    'stirring_speed': 300,  # rpm
                    'order': 'slow_addition'
                },
                {
                    'step': 'film_deposition',
                    'method': 'spin_coating',
                    'speed': 4000,  # rpm
                    'time': 30,  # seconds
                    'acceleration': 2000  # rpm/s
                }
            ],
            'crystallization': crystallization,
            'post_processing': [
                {
                    'step': 'annealing',
                    'temperature': crystallization['temperature'],
                    'time': crystallization['time'],
                    'atmosphere': 'nitrogen',
                    'ramp_rate': 5  # °C/min
                }
            ]
        }
        
        return protocol
    
    async def optimize_conditions(self, 
                                protocol: Dict[str, Any],
                                previous_results: List[SynthesisResult]) -> Dict[str, Any]:
        """Optimize synthesis conditions based on previous results"""
        try:
            # Analyze previous results
            optimization_targets = await self._analyze_previous_results(previous_results)
            
            # Apply optimization algorithms
            if optimization_targets['improve_yield']:
                protocol = await self._optimize_for_yield(protocol, previous_results)
            
            if optimization_targets['improve_purity']:
                protocol = await self._optimize_for_purity(protocol, previous_results)
            
            if optimization_targets['improve_crystallinity']:
                protocol = await self._optimize_for_crystallinity(protocol, previous_results)
            
            # Update protocol with optimized parameters
            protocol['optimization_history'] = [
                {
                    'timestamp': datetime.now(),
                    'targets': optimization_targets,
                    'changes_made': protocol.get('recent_changes', [])
                }
            ]
            
            return protocol
            
        except Exception as e:
            logger.error(f"Error optimizing synthesis conditions: {e}")
            raise SynthesisError(f"Condition optimization failed: {e}")
    
    async def plan_precursor_preparation(self, 
                                       precursors: Dict[str, float]) -> List[Dict[str, Any]]:
        """Plan precursor preparation and purification steps"""
        try:
            preparation_steps = []
            
            for precursor, amount in precursors.items():
                # Check purity requirements
                purity_requirement = await self._get_purity_requirement(precursor)
                
                # Design purification protocol if needed
                if purity_requirement > 0.99:  # High purity required
                    purification_steps = await self._design_purification_protocol(precursor)
                    preparation_steps.extend(purification_steps)
                
                # Calculate required quantities with safety margin
                required_amount = amount * 1.2  # 20% safety margin
                
                # Check availability and ordering
                availability = await self.experimental_db.check_precursor_availability(precursor)
                
                step = {
                    'precursor': precursor,
                    'required_amount': required_amount,
                    'unit': 'g',
                    'purity_requirement': purity_requirement,
                    'availability': availability,
                    'preparation_time': self._estimate_preparation_time(precursor),
                    'storage_conditions': await self._get_storage_conditions(precursor)
                }
                
                preparation_steps.append(step)
            
            return preparation_steps
            
        except Exception as e:
            logger.error(f"Error planning precursor preparation: {e}")
            raise SynthesisError(f"Precursor preparation planning failed: {e}")
    
    async def monitor_synthesis(self, 
                              batch_id: str,
                              protocol: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor synthesis progress and adjust parameters if needed"""
        try:
            # Initialize monitoring
            monitoring_data = {
                'batch_id': batch_id,
                'start_time': datetime.now(),
                'current_step': 0,
                'total_steps': len(protocol['preparation_steps']),
                'status': 'in_progress',
                'measurements': []
            }
            
            # Monitor each step
            for step_idx, step in enumerate(protocol['preparation_steps']):
                monitoring_data['current_step'] = step_idx + 1
                
                # Step-specific monitoring
                if step['step'] == 'precursor_dissolution':
                    await self._monitor_dissolution(batch_id, step)
                elif step['step'] == 'solution_mixing':
                    await self._monitor_mixing(batch_id, step)
                elif step['step'] == 'film_deposition':
                    await self._monitor_deposition(batch_id, step)
                
                # Check for anomalies
                anomalies = await self._check_for_anomalies(batch_id, step)
                if anomalies:
                    # Adjust parameters if needed
                    adjustments = await self._suggest_adjustments(anomalies)
                    monitoring_data['adjustments'] = adjustments
            
            monitoring_data['status'] = 'completed'
            monitoring_data['end_time'] = datetime.now()
            
            return monitoring_data
            
        except Exception as e:
            logger.error(f"Error monitoring synthesis {batch_id}: {e}")
            raise SynthesisError(f"Synthesis monitoring failed: {e}")
    
    async def analyze_batch_quality(self, 
                                  batch_id: str,
                                  composition: str) -> SynthesisResult:
        """Analyze quality of synthesized batch"""
        try:
            # Collect measurement data
            measurements = await self.experimental_db.get_batch_measurements(batch_id)
            
            # Analyze yield
            yield_percentage = await self._calculate_yield(measurements)
            
            # Analyze purity
            purity = await self._calculate_purity(measurements)
            
            # Calculate quality metrics
            quality_metrics = {
                'crystallinity': await self._calculate_crystallinity(measurements),
                'surface_roughness': await self._calculate_surface_roughness(measurements),
                'defect_density': await self._calculate_defect_density(measurements),
                'optical_quality': await self._calculate_optical_quality(measurements)
            }
            
            # Get synthesis conditions
            conditions = await self.experimental_db.get_synthesis_conditions(batch_id)
            
            result = SynthesisResult(
                composition=composition,
                synthesis_method=conditions['method'],
                conditions=conditions,
                yield_percentage=yield_percentage,
                purity=purity,
                batch_id=batch_id,
                timestamp=datetime.now(),
                quality_metrics=quality_metrics
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing batch quality for {batch_id}: {e}")
            raise SynthesisError(f"Batch quality analysis failed: {e}")
    
    def handoff_to_characterization(self, synthesis_results: List[SynthesisResult]):
        """Hand off synthesized materials to characterization agent"""
        # Prepare characterization request
        characterization_request = {
            'materials': [
                {
                    'batch_id': result.batch_id,
                    'composition': result.composition,
                    'synthesis_method': result.synthesis_method,
                    'expected_properties': result.quality_metrics,
                    'priority': 'high' if result.yield_percentage > 80 else 'medium'
                }
                for result in synthesis_results
            ],
            'characterization_suite': [
                'xrd_structure_analysis',
                'uv_vis_optical_properties',
                'plqy_quantum_yield',
                'sem_morphology',
                'stability_testing'
            ],
            'timeline': '24_hours'
        }
        
        return self.handoff(
            "CharacterizationAgent",
            characterization_request=characterization_request,
            context="Fresh synthesis batches requiring comprehensive characterization"
        )
    
    def handoff_to_optimization(self, synthesis_results: List[SynthesisResult]):
        """Hand off results to optimization agent for process improvement"""
        optimization_request = {
            'synthesis_results': [result.__dict__ for result in synthesis_results],
            'optimization_targets': {
                'yield_threshold': 85.0,
                'purity_threshold': 95.0,
                'crystallinity_threshold': 90.0
            },
            'constraints': {
                'temperature_max': 200,  # °C
                'time_max': 120,  # minutes
                'cost_max': 50  # $/g
            }
        }
        
        return self.handoff(
            "OptimizationAgent",
            optimization_request=optimization_request,
            context="Synthesis results requiring process optimization"
        )
    
    # Helper methods (abbreviated for space)
    def _select_optimal_method(self, composition: str, target_properties: Dict[str, float]) -> str:
        """Select optimal synthesis method based on composition and targets"""
        # Implementation logic here
        return "solution_processing"
    
    async def _select_solvent_system(self, precursors: Dict[str, float]) -> Dict[str, str]:
        """Select optimal solvent system"""
        # Implementation logic here
        return {"primary": "DMF", "secondary": "DMSO", "ratio": "4:1"}

    async def _calculate_concentrations(self, precursors: Dict[str, float], solvent_system: Dict[str, str]) -> Dict[str, float]:
        """Calculate precursor concentrations for solution processing."""
        # Calculate molarity based on synthesis parameters
        # Using standard concentration of 1.0 M for perovskite precursors
        return {precursor: 1.0 for precursor in precursors}
    
    async def _design_crystallization_conditions(self, target_properties: Dict[str, float]) -> Dict[str, float]:
        """Design crystallization conditions for solution processing."""
        # For now, return a default set of conditions
        return {"temperature": 100, "time": 30}

    async def _generate_safety_protocol(self, precursors: Dict[str, float]) -> Dict[str, str]:
        """Generate safety protocol for synthesis."""
        return {"level": "standard", "notes": "Wear gloves and use fume hood."}

    def _estimate_synthesis_time(self, protocol: dict) -> float:
        """Estimate synthesis time in hours."""
        return 2.0

    def _list_required_equipment(self, protocol: dict) -> list:
        """List required equipment for synthesis protocol."""
        return ["magnetic_stirrer", "hotplate", "spin_coater", "fume_hood"]

    # Additional helper methods...