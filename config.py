import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MURF_API_KEY = os.getenv("MURF_API_KEY")

    UPLOAD_FOLDER = "uploads"
    STATIC_FOLDER = "static"
    GEMINI_MODEL = "gemini-2.5-flash"

    @classmethod
    def validate(cls):
        missing = []
        if not cls.ASSEMBLYAI_API_KEY:
            missing.append("ASSEMBLYAI_API_KEY")
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not cls.MURF_API_KEY:
            missing.append("MURF_API_KEY")
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
