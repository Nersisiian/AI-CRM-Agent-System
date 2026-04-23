from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = Field(None)

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: List[str] = []
