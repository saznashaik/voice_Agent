import google.generativeai as genai
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel(Config.GEMINI_MODEL)

def generate_response(prompt: str) -> str:
    try:
        logger.debug(f"Generating LLM response for prompt length={len(prompt)}")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise
