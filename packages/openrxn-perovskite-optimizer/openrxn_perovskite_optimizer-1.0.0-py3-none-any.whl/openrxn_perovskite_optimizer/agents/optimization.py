from typing import Dict, List, Any
import logging
from dataclasses import dataclass
from agents import Agent

from ..ml.optimization import GeneticOptimizer
from ..utils.exceptions import OptimizationError

logger = logging.getLogger(__name__)

@dataclass
class OptimizationResult:
    """Results from optimization process"""
    best_composition: str
    best_score: float
    optimized_parameters: Dict[str, Any]
    convergence_history: List[float]

class OptimizationAgent(Agent):
    """AI agent for process and materials optimization"""
    
    def __init__(self, optimizer: GeneticOptimizer):
        super().__init__(
            name="OptimizationAgent",
            instructions="""
            You are an expert in process and materials optimization.
            Your role is to:
            1. Optimize synthesis conditions for target properties
            2. Optimize device architecture for performance
            3. Use genetic algorithms and Bayesian optimization
            4. Suggest new experiments to accelerate discovery
            """,
            model="gpt-4o",
            tools=[]
        )
        self.optimizer = optimizer