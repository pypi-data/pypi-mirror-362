from pydantic import BaseModel
from typing import Dict, Any

class ProtocolIn(BaseModel):
    protocol: Dict[str, Any]

class ProtocolOut(BaseModel):
    status: str
    result: Dict[str, Any]