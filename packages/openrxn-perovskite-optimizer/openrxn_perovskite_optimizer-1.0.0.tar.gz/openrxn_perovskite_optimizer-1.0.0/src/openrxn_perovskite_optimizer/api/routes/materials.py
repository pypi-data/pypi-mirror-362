from fastapi import APIRouter, Depends
from typing import List
from ...agents.discovery import MaterialsDiscoveryAgent, DiscoveryResult
from ..dependencies import get_discovery_agent

router = APIRouter()

@router.post("/discover", response_model=List[DiscoveryResult])
async def discover_materials(
    composition: str,
    discovery_agent: MaterialsDiscoveryAgent = Depends(get_discovery_agent),
) -> List[DiscoveryResult]:
    """
    Discovers new perovskite materials using the discovery agent.
    """
    results = await discovery_agent.discover_materials(
        target_properties={"efficiency": 25.0, "stability": 1000.0},
        max_candidates=10
    )
    return results