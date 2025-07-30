from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from ...agents.experimental import ExperimentalAgent
from ..dependencies import get_experimental_agent

router = APIRouter()

@router.post("/execute")
async def execute_experiment(
    protocol: Dict[str, Any],
    experimental_agent: ExperimentalAgent = Depends(get_experimental_agent),
) -> Dict[str, Any]:
    """
    Executes a synthesis or characterization protocol.
    """
    result = await experimental_agent.execute_protocol(protocol)
    return result