# 🎤 30 Days of Voice Agents — Conversational Echo Bot (ELSA)

A real-time **voice agent** built with **Flask**, **AssemblyAI Speech-to-Text**, **Google Gemini LLM**, and **Murf.ai Text-to-Speech**.  
This bot listens to your voice, transcribes it, processes your request with an LLM, and responds back with generated human-like speech — preserving conversation history.

---

## 📌 Features

- **Real-time voice interaction** via AssemblyAI STT.
- **Elsa persona (Frozen)** using Gemini LLM:
  - Speaks elegantly and empathetically.
  - Avoids verbatim copyrighted lyrics.
- **TTS** with Murf AI streamed directly to speakers.
- **Web context & news integration**:
  - Fetches relevant web results via Tavily.
  - Retrieves latest news headlines.
- **Flask-based UI** with:
  - Start/Stop recording buttons.
  - API key configuration modal.
  - Live chat display with user and Elsa messages.
- **Persistent conversation history** (per `session_id`) stored in JSONL.
- **Fallback handling** if any API fails (returns default audio + message).
- Automatic text shortening for TTS if over character limit.
- Simple **REST API** for other clients.
---

## 🛠️ Tech Stack

**Backend:**
- Python 3.x
- Flask
- Requests
- AssemblyAI Python SDK (`assemblyai`)
- Google Generative AI SDK (`google-generativeai`)
- Python-dotenv

**Frontend:**
- HTML / CSS / JavaScript
- Native MediaRecorder API for recording
- Fetch API for communication

---

## 🏗️ Architecture
    🎤 User Speaks
            ↓ 
    (Browser Microphone)[ MediaRecorder API in Browser ]
            ↓
    🎧 Audio sent to Flask /agent/chat/<session_id>
            ↓
    (1) 📜 STT via AssemblyAI → Transcript
    (2) 🤖 Gemini LLM → Generates AI Response
    (3) 🔊 Murf TTS → Converts Response to Speech
            ↓
    📦 Flask stores and serves audio from /static
            ↓
    🔁 Browser plays AI voice + updates conversation view


---

## 📂 Project Structure

    voice_agent_app/
    │
    ├── app.py 
    ├── streaming_app.py          #for streaming
    ├── config.py               # API keys, folder paths
    ├── schemas/                # Pydantic request/response models
    │   ├── __init__.py
    │   ├── llm.py
    │   ├── tts.py
    │   ├── stt.py
    │   ├── agent.py
    │
    ├── services/               # Wrappers for 3rd party APIs
    │   ├── __init__.py
    │   ├── llm_service.py
    │   ├── stt_service.py
    │   ├── tts_service.py
    │
    ├── utils/                  
    │   ├── __init__.py
    │   ├── logger.py           # Logging setup
    │
    ├── static/
    ├── templates/
    └── requirements.txt


---
⚡ Key Components

    | Component              | Description                                                    |
    | ---------------------- | -------------------------------------------------------------- |
    | **AssemblyAIRealtime** | Streams microphone input and returns live transcripts.         |
    | **GeminiLLM**          | Generates Elsa persona responses, streaming output chunk-wise. |
    | **MurfStreamer**       | Converts text chunks to TTS audio streamed to speakers.        |
    | **RelayServer**        | WebSocket relay to broadcast messages/audio to browser.        |
    | **VoiceAgent**         | Coordinates STT → LLM → TTS pipeline and handles chat history. |
    | **Flask UI**           | Web interface with recording, API keys, and chat display.      |

🙏 Acknowledgements

    AssemblyAI
     — Realtime STT
    
    Google Gemini
     — LLM API
    
    Murf
     — TTS
    
    Tavily
     — Web search API
    
    NewsAPI
     — Latest news

## 🔑 Environment Variables

    Create a `.env` file in the project root:
        ASSEMBLYAI_API_KEY=your_assemblyai_api_key
        MURF_API_KEY=your_murf_api_key
        GEMINI_API_KEY=your_gemini_api_key
        TAVILY_API_KEY=your_tavily_key
        NEWS_API_KEY=your_news_key

Make sure you have valid API keys for all three services.

---

## 🚀 Running Locally

    1️⃣ **Clone the repository**
        git clone https://github.com/yourusername/voice-agent.git
        cd voice-agent


    2️⃣ **Create and activate a virtual environment**
        python -m venv venv
        source venv/bin/activate # On macOS/Linux
        venv\Scripts\activate # On Windows


    3️⃣ **Install dependencies**
        pip install -r requirements.txt


    4️⃣ **Set environment variables**
        cp .env.example .env

        Fill in your API keys inside .env


    5️⃣ **Run the Flask server**
        python app.py


    Access: http://localhost:5000
    
    Start recording with Start Recording button.
    
    Stop recording with Stop Recording.
    
    Configure API keys anytime via ⚙️.
---

## 📡 API Endpoints

### **1. Transcribe Only**
    `POST /tts/echo`
        - **Form-Data**: `audio` (Uploaded audio file)
        - **Response**:
            {
            "transcript": "Hello world"
            }

---

    ### **2. LLM Query**
        `POST /llm/query`
        - **JSON body**:
            {
            "text": "Write a haiku about the ocean"
            }

        - **Response**:
            {
            "response": "Calm waves drift ashore..."
            }


    ---

    ### **3. Generate TTS from Transcript**
        `POST /generate-murf-from-transcript`
        - **JSON body**:
            {
            "transcript": "Your AI generated text here..."
            }

        - **Response**:
            {
            "audio_url": "/static/murf_xxx.mp3"
            }
        

    ---

    ### **4. Conversational Agent**
        `POST /agent/chat/<session_id>`
        - **Form-Data**: `audio` (User's voice)
        - **Response**:
        {
        "session_id": "s_1720000000000",
        "transcript": "User text",
        "response_text": "Bot reply",
        "audio_url": "/static/murf_s_1720000000000.mp3"
        }



