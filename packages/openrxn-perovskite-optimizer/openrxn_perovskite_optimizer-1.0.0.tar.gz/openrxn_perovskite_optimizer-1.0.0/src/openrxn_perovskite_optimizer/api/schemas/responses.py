from pydantic import BaseModel
from typing import List, Dict, Any

class StatusResponse(BaseModel):
    status: str
    message: str = None

class ErrorResponse(BaseModel):
    error: str
    details: Dict[str, Any] = None