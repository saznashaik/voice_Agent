from pydantic import BaseModel

class MurfRequest(BaseModel):
    transcript: str

class MurfResponse(BaseModel):
    audio_url: str
