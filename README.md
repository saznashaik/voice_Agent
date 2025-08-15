# 🎤 30 Days of Voice Agents — Conversational Echo Bot

A real-time **voice agent** built with **Flask**, **AssemblyAI Speech-to-Text**, **Google Gemini LLM**, and **Murf.ai Text-to-Speech**.  
This bot listens to your voice, transcribes it, processes your request with an LLM, and responds back with generated human-like speech — preserving conversation history.

---

## 📌 Features

- **Speech-to-Text (STT)** with [AssemblyAI](https://www.assemblyai.com/)  
- **Conversational AI** with [Google Gemini](https://ai.google/google-gemini/)  
- **Text-to-Speech (TTS)** with [Murf.ai](https://murf.ai/)  
- **Persistent Conversation History** in memory (per `session_id`)  
- Interactive **web interface** with start/stop recording controls  
- **Fallback handling** if any API call fails (returns default audio + message)  
- Automatic text shortening for TTS if over character limit  
- Simple **REST API** to use from other clients

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
   flowchart TD
  %% Sections
  subgraph Client[Client (Browser)]
    Mic[🎤 Record audio (MediaRecorder)]
    UI[🖥️ Conversation UI]
  end

  subgraph Server[Flask Server]
    Route[/POST /agent/chat/<session_id>/]
    Store[📦 Save MP3 to /static]
    Hist[🗂️ In‑memory chat history]
  end

  subgraph Services[Service Layer]
    STT[📜 STT: AssemblyAI]
    LLM[🤖 LLM: Gemini]
    TTS[🔊 TTS: Murf]
  end

  %% Flow
  Mic -->|audio/webm| Route
  UI -->|Start/Stop| Mic

  %% (1) STT
  Route -->|1) Transcribe| STT
  STT -->|Transcript| Route

  %% (2) LLM
  Route -->|2) Prompt + History| LLM
  LLM -->|AI Response Text| Route
  Route --> Hist

  %% (3) TTS
  Route -->|3) Synthesize| TTS
  TTS -->|MP3 bytes| Store
  Store -->|/static/<file>.mp3| UI

  %% Playback + UI update
  UI -->|Play AI voice| UI
  UI -->|Update chat view| UI



---

## 📂 Project Structure

project/
│
├── app.py # Flask backend
├── templates/
│ └── index.html # Web interface
├── static/
│ ├── script.js # Client-side JS logic
│ ├── style.css # UI styles
│ └── fallback.mp3 # Optional fallback audio
├── uploads/ # Temp uploaded audio files
├── .env # API keys (not tracked in git)
├── requirements.txt
└── README.md # You are here

---

## 🔑 Environment Variables

Create a `.env` file in the project root:
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    MURF_API_KEY=your_murf_api_key
    GEMINI_API_KEY=your_gemini_api_key


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




