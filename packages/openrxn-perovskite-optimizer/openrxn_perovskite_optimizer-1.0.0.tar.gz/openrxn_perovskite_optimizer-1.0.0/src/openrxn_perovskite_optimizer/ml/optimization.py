"""
Genetic algorithm optimization for perovskite materials.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

import numpy as np
import asyncio
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
import random
import re

@dataclass
class OptimizationResult:
    """Result from optimization process"""
    best_composition: str
    best_score: float
    best_properties: Dict[str, float]
    convergence_history: List[float]
    generation_count: int
    population_diversity: float

class GeneticOptimizer:
    """Genetic algorithm optimizer for perovskite compositions"""
    
    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.fitness_scores = []
        self.convergence_history = []
        
    async def optimize_composition(self, 
                                 base_composition: str, 
                                 objective: str, 
                                 max_iterations: int, 
                                 population_size: int, 
                                 progress_callback: Optional[Callable[[int], None]] = None) -> Dict[str, Any]:
        """
        Optimize perovskite composition using genetic algorithm
        
        Args:
            base_composition: Starting composition (e.g., "MAPbI3")
            objective: Optimization objective ("efficiency", "stability", "cost", "multi")
            max_iterations: Maximum number of generations
            population_size: Size of population per generation
            progress_callback: Callback function for progress updates
            
        Returns:
            Dictionary with optimization results
        """
        
        # Initialize population
        self.population = self._initialize_population(base_composition, population_size)
        self.convergence_history = []
        
        best_individual = None
        best_score = float('-inf')
        
        for generation in range(max_iterations):
            # Evaluate fitness for each individual
            fitness_scores = []
            for individual in self.population:
                score = await self._evaluate_fitness(individual, objective)
                fitness_scores.append(score)
            
            self.fitness_scores = fitness_scores
            
            # Track best individual
            gen_best_idx = np.argmax(fitness_scores)
            gen_best_score = fitness_scores[gen_best_idx]
            
            if gen_best_score > best_score:
                best_score = gen_best_score
                best_individual = self.population[gen_best_idx]
            
            # Record convergence
            self.convergence_history.append(best_score)
            
            # Progress callback
            if progress_callback:
                progress_callback(generation)
            
            # Early stopping if converged
            if generation > 10 and self._check_convergence():
                break
            
            # Create next generation
            if generation < max_iterations - 1:
                self.population = self._create_next_generation()
        
        # Calculate final properties
        final_properties = await self._calculate_properties(best_individual or base_composition)
        
        return {
            'best_composition': best_individual,
            'best_score': best_score,
            'best_properties': final_properties,
            'convergence_history': self.convergence_history,
            'generation_count': len(self.convergence_history),
            'population_diversity': self._calculate_diversity()
        }
    
    def _initialize_population(self, base_composition: str, population_size: int) -> List[str]:
        """Initialize population with variations of base composition"""
        population = [base_composition]  # Include original
        
        # Parse base composition
        elements = self._parse_composition(base_composition)
        
        # Generate variations
        for _ in range(population_size - 1):
            new_composition = self._mutate_composition(elements)
            population.append(new_composition)
        
        return population
    
    def _parse_composition(self, composition: str) -> Dict[str, float]:
        """Parse composition string into elements and ratios"""
        # Simplified parser for perovskite compositions
        elements = {}
        
        # Handle common perovskite patterns
        if "MA" in composition:
            elements["MA"] = 1.0
        if "FA" in composition:
            elements["FA"] = 1.0
        if "Cs" in composition:
            elements["Cs"] = 1.0
        if "Pb" in composition:
            elements["Pb"] = 1.0
        if "I" in composition:
            elements["I"] = 3.0
        if "Br" in composition:
            elements["Br"] = 3.0
        if "Cl" in composition:
            elements["Cl"] = 3.0
        
        # Handle mixed compositions (simplified)
        if "0." in composition:
            # Extract numerical coefficients
            numbers = re.findall(r'(\d+\.?\d*)', composition)
            if len(numbers) >= 2:
                elements["MA"] = float(numbers[0]) if "MA" in composition else 0.0
                elements["FA"] = float(numbers[1]) if "FA" in composition else 0.0
                elements["Cs"] = 1.0 - elements["MA"] - elements["FA"] if "Cs" in composition else 0.0
        
        return elements
    
    def _mutate_composition(self, elements: Dict[str, float]) -> str:
        """Create mutated composition"""
        mutated = elements.copy()
        
        # Mutate A-site cations (MA, FA, Cs)
        a_site_cations = ["MA", "FA", "Cs"]
        a_site_present = [k for k in a_site_cations if k in mutated and mutated[k] > 0]
        
        if len(a_site_present) > 1:
            # Adjust ratios
            for cation in a_site_present:
                if random.random() < self.mutation_rate:
                    mutated[cation] += random.uniform(-0.1, 0.1)
                    mutated[cation] = max(0.0, min(1.0, mutated[cation]))
            
            # Normalize A-site
            total_a = sum(mutated.get(c, 0) for c in a_site_cations)
            if total_a > 0:
                for cation in a_site_cations:
                    if cation in mutated:
                        mutated[cation] /= total_a
        
        # Mutate X-site anions (I, Br, Cl)
        x_site_anions = ["I", "Br", "Cl"]
        x_site_present = [k for k in x_site_anions if k in mutated and mutated[k] > 0]
        
        if len(x_site_present) > 1:
            for anion in x_site_present:
                if random.random() < self.mutation_rate:
                    mutated[anion] += random.uniform(-0.3, 0.3)
                    mutated[anion] = max(0.0, min(3.0, mutated[anion]))
            
            # Normalize X-site to 3.0
            total_x = sum(mutated.get(a, 0) for a in x_site_anions)
            if total_x > 0:
                for anion in x_site_anions:
                    if anion in mutated:
                        mutated[anion] = mutated[anion] / total_x * 3.0
        
        return self._composition_to_string(mutated)
    
    def _composition_to_string(self, elements: Dict[str, float]) -> str:
        """Convert element dictionary back to composition string"""
        # Simplified composition string generation
        result = ""
        
        # A-site cations
        a_site = ["MA", "FA", "Cs"]
        a_present = [(k, v) for k, v in elements.items() if k in a_site and v > 0.01]
        
        if len(a_present) == 1:
            result += a_present[0][0]
        else:
            # Mixed A-site
            for i, (cation, ratio) in enumerate(sorted(a_present, key=lambda x: x[1], reverse=True)):
                if i > 0:
                    result += f"{ratio:.1f}"
                result += cation
        
        # B-site (always Pb for perovskites)
        result += "Pb"
        
        # X-site anions
        x_site = ["I", "Br", "Cl"]
        x_present = [(k, v) for k, v in elements.items() if k in x_site and v > 0.01]
        
        if len(x_present) == 1:
            anion, count = x_present[0]
            if abs(count - 3.0) < 0.1:
                result += f"{anion}3"
            else:
                result += f"{anion}{count:.1f}"
        else:
            # Mixed X-site
            for anion, count in sorted(x_present, key=lambda x: x[1], reverse=True):
                if abs(count - round(count)) < 0.1:
                    result += f"{anion}{int(round(count))}"
                else:
                    result += f"{anion}{count:.1f}"
        
        return result
    
    async def _evaluate_fitness(self, composition: str, objective: str) -> float:
        """Evaluate fitness of a composition"""
        # Simulate property calculation
        properties = await self._calculate_properties(composition)
        
        if objective == "efficiency":
            return properties["efficiency"]
        elif objective == "stability":
            return properties["stability"]
        elif objective == "cost":
            return 1.0 / properties["cost"]  # Lower cost = higher fitness
        elif objective == "multi":
            # Multi-objective optimization
            return (
                0.4 * properties["efficiency"] / 25.0 +
                0.3 * properties["stability"] / 2000.0 +
                0.3 * (1.0 / properties["cost"]) / 0.1
            )
        else:
            return properties["efficiency"]
    
    async def _calculate_properties(self, composition: str) -> Dict[str, float]:
        """Calculate properties for a composition (simplified simulation)"""
        # Simulate property calculation based on composition
        hash_val = hash(composition)
        
        # Base properties with some composition-dependent variation
        base_efficiency = 18.0
        base_stability = 1000.0
        base_cost = 0.2
        
        # Add composition-dependent effects
        if "MA" in composition:
            base_efficiency += 2.0
            base_stability -= 200.0
            base_cost -= 0.05
        
        if "FA" in composition:
            base_efficiency += 3.0
            base_stability += 100.0
            base_cost += 0.02
        
        if "Cs" in composition:
            base_efficiency -= 1.0
            base_stability += 500.0
            base_cost += 0.08
        
        if "Br" in composition:
            base_efficiency -= 5.0
            base_stability += 800.0
            base_cost += 0.03
        
        # Add random variation
        efficiency = base_efficiency + (hash_val % 100) / 100.0 * 4.0 - 2.0
        stability = base_stability + (hash_val % 1000) - 500.0
        cost = base_cost + (hash_val % 50) / 1000.0
        
        return {
            "efficiency": max(5.0, min(30.0, efficiency)),
            "stability": max(100.0, min(3000.0, stability)),
            "cost": max(0.05, min(1.0, cost))
        }
    
    def _create_next_generation(self) -> List[str]:
        """Create next generation through selection, crossover, and mutation"""
        next_generation = []
        
        # Elite selection (keep best individuals)
        elite_count = max(1, len(self.population) // 10)
        elite_indices = np.argsort(self.fitness_scores)[-elite_count:]
        for idx in elite_indices:
            next_generation.append(self.population[idx])
        
        # Fill rest through crossover and mutation
        while len(next_generation) < len(self.population):
            if random.random() < self.crossover_rate and len(next_generation) < len(self.population) - 1:
                # Crossover
                parent1, parent2 = self._select_parents()
                child1, child2 = self._crossover(parent1, parent2)
                next_generation.extend([child1, child2])
            else:
                # Mutation
                parent = self._select_parent()
                child = self._mutate_individual(parent)
                next_generation.append(child)
        
        return next_generation[:len(self.population)]
    
    def _select_parents(self) -> tuple:
        """Select two parents using tournament selection"""
        parent1 = self._select_parent()
        parent2 = self._select_parent()
        return parent1, parent2
    
    def _select_parent(self) -> str:
        """Select parent using tournament selection"""
        tournament_size = 3
        tournament_indices = random.sample(range(len(self.population)), 
                                         min(tournament_size, len(self.population)))
        
        best_idx = max(tournament_indices, key=lambda i: self.fitness_scores[i])
        return self.population[best_idx]
    
    def _crossover(self, parent1: str, parent2: str) -> tuple:
        """Perform crossover between two parents"""
        # Simple crossover for perovskite compositions
        elements1 = self._parse_composition(parent1)
        elements2 = self._parse_composition(parent2)
        
        child1_elements = {}
        child2_elements = {}
        
        # Mix elements
        for element in set(elements1.keys()) | set(elements2.keys()):
            val1 = elements1.get(element, 0.0)
            val2 = elements2.get(element, 0.0)
            
            # Weighted average with some randomness
            alpha = random.uniform(0.3, 0.7)
            child1_elements[element] = alpha * val1 + (1 - alpha) * val2
            child2_elements[element] = (1 - alpha) * val1 + alpha * val2
        
        return (self._composition_to_string(child1_elements),
                self._composition_to_string(child2_elements))
    
    def _mutate_individual(self, individual: str) -> str:
        """Mutate an individual"""
        elements = self._parse_composition(individual)
        return self._mutate_composition(elements)
    
    def _check_convergence(self) -> bool:
        """Check if optimization has converged"""
        if len(self.convergence_history) < 5:
            return False
        
        recent_scores = self.convergence_history[-5:]
        return max(recent_scores) - min(recent_scores) < 0.001
    
    def _calculate_diversity(self) -> float:
        """Calculate population diversity"""
        if len(self.population) < 2:
            return 0.0
        
        unique_compositions = set(self.population)
        return len(unique_compositions) / len(self.population)


class DigitalTwinOptimizer:
    """Optimizer for digital twin models"""
    
    def __init__(self, digital_twin):
        self.digital_twin = digital_twin
    
    async def optimize(self, 
                      target_properties: Dict[str, float], 
                      variables: List[str], 
                      max_iterations: int) -> Any:
        """Optimize digital twin parameters"""
        
        # Placeholder implementation
        class OptimizationResult:
            def __init__(self, digital_twin):
                self.best_structure = digital_twin.structure if hasattr(digital_twin, 'structure') else None
                self.best_properties = target_properties.copy()
                self.history = []
                self.convergence = []
        
        # Simulate optimization process
        result = OptimizationResult(self.digital_twin)
        
        for i in range(max_iterations):
            # Simulate optimization step
            await asyncio.sleep(0.001)  # Small delay to simulate computation
            
            # Add some convergence history
            score = 0.8 + 0.2 * np.exp(-i / 20) + np.random.normal(0, 0.02)
            result.convergence.append(score)
            
            result.history.append({
                'iteration': i,
                'score': score,
                'variables': {var: np.random.random() for var in variables}
            })
        
        return result