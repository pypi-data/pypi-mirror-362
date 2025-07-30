from pydantic import BaseModel
from typing import List, Dict, Any

class PerovskiteMaterial(BaseModel):
    composition: str
    properties: Dict[str, Any]

class DiscoveryIn(BaseModel):
    base_composition: str
    target_properties: Dict[str, float]

class DiscoveryOut(BaseModel):
    results: List[PerovskiteMaterial]