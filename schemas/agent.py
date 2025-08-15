from pydantic import BaseModel
from typing import Optional

class AgentChatResponse(BaseModel):
    session_id: str
    transcript: str
    response_text: str
    audio_url: str
    error: Optional[str] = None
