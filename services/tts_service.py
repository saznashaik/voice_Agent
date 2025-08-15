import requests
import os
from werkzeug.utils import secure_filename
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_murf_audio(text: str, filename: str) -> str:
    headers = {
        "api-key": Config.MURF_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "voiceId": "en-US-natalie",
        "format": "MP3",
        "sampleRate": 24000,
        "modelVersion": "GEN2"
    }
    try:
        r = requests.post("https://api.murf.ai/v1/speech/generate", json=payload, headers=headers)
        r.raise_for_status()
        audio_url = r.json().get("audioFile")
        if not audio_url:
            raise ValueError("No audioFile in Murf response")

        audio_resp = requests.get(audio_url)
        audio_resp.raise_for_status()
        output_path = os.path.join(Config.STATIC_FOLDER, filename)
        with open(output_path, "wb") as f:
            f.write(audio_resp.content)
        return f"/static/{filename}"
    except Exception as e:
        logger.error(f"Murf TTS failed: {e}")
        raise
