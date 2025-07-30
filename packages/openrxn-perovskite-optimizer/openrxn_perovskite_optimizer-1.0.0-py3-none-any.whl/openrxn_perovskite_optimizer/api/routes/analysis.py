from fastapi import APIRouter, Depends
from typing import Dict, Any
from ...agents.characterization import CharacterizationAgent, CharacterizationResult
from ..dependencies import get_characterization_agent

router = APIRouter()

@router.post("/analyze", response_model=CharacterizationResult)
async def analyze_data(
    data: Dict[str, Any],
    characterization_agent: CharacterizationAgent = Depends(get_characterization_agent),
) -> CharacterizationResult:
    """
    Analyzes experimental data using the characterization agent.
    """
    result = await characterization_agent.analyze_data(data)
    return result