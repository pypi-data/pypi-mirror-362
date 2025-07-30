from fastapi import APIRouter, Depends
from ...agents.optimization import OptimizationAgent, OptimizationResult
from ..dependencies import get_optimization_agent

router = APIRouter()

@router.post("/optimize", response_model=OptimizationResult)
async def optimize_composition(
    composition: str,
    optimization_agent: OptimizationAgent = Depends(get_optimization_agent),
) -> OptimizationResult:
    """
    Optimizes a perovskite composition using the optimization agent.
    """
    result = await optimization_agent.optimize_composition(
        base_composition=composition,
        objective="multi",
        max_iterations=100,
        population_size=50,
        progress_callback=lambda x: None
    )
    return result