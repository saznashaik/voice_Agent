import assemblyai as aai
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
aai.settings.api_key = Config.ASSEMBLYAI_API_KEY

def transcribe_audio(file_path: str) -> str:
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        return transcript.text
    except Exception as e:
        logger.error(f"STT Transcription error: {e}")
        raise
