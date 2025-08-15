from flask import Flask, jsonify, request, render_template
from config import Config
from schemas.tts import MurfRequest, MurfResponse
from schemas.llm import LLMRequest, LLMResponse
from schemas.agent import AgentChatResponse
from services.stt_service import transcribe_audio
from services.llm_service import generate_response
from services.tts_service import generate_murf_audio
from utils.logger import setup_logger
from werkzeug.utils import secure_filename
import time, os

Config.validate()
app = Flask(__name__, static_folder="static", template_folder="templates")
logger = setup_logger(__name__)
CHAT_HISTORIES = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/llm/query", methods=["POST"])
def llm_query():
    try:
        req = LLMRequest(**request.get_json())
        result = generate_response(req.text)
        return jsonify(LLMResponse(response=result).dict())
    except Exception as e:
        logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route("/tts/echo", methods=["POST"])
def tts_echo():
    if "audio" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    audio_file = request.files["audio"]
    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    audio_file.save(filepath)
    try:
        transcript = transcribe_audio(filepath)
        return jsonify({"transcript": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)

@app.route("/generate-murf-from-transcript", methods=["POST"])
def generate_from_transcript():
    try:
        req = MurfRequest(**request.get_json())
        fname = secure_filename(f"murf_{int(time.time()*1000)}.mp3")
        url = generate_murf_audio(req.transcript, fname)
        return jsonify(MurfResponse(audio_url=url).dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/agent/chat/<session_id>", methods=["POST"])
def agent_chat(session_id):
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"error": "No audio provided"}), 400
    filename = secure_filename(audio_file.filename or "recording.webm")
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    audio_file.save(filepath)

    try:
        user_text = transcribe_audio(filepath)
    except:
        user_text = "[STT failed]"

    history = CHAT_HISTORIES.setdefault(session_id, [])
    history.append({"role": "user", "content": user_text})

    try:
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history]) + "\nassistant:"
        assistant_text = generate_response(prompt)
    except:
        assistant_text = "I'm having trouble connecting right now."

    history.append({"role": "assistant", "content": assistant_text})

    try:
        fname = secure_filename(f"murf_{session_id}_{int(time.time()*1000)}.mp3")
        audio_url = generate_murf_audio(assistant_text, fname)
    except:
        audio_url = "/static/fallback.mp3"

    return jsonify(AgentChatResponse(
        session_id=session_id,
        transcript=user_text,
        response_text=assistant_text,
        audio_url=audio_url
    ).dict())

if __name__ == "__main__":
    # Use single-process Flask dev server for in-memory chat store
    app.run(debug=True, port=5001)
