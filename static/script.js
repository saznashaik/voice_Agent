// static/script.js
let mediaRecorder;
let recordedChunks = [];
let sessionId = null;

function getOrCreateSessionId() {
  const params = new URLSearchParams(window.location.search);
  let sid = params.get("session_id");
  if (!sid) {
    sid = `s_${Date.now()}`;
    params.set("session_id", sid);
    const newUrl = window.location.pathname + "?" + params.toString();
    history.replaceState({}, "", newUrl);
  }
  return sid;
}

function setSessionDisplay(sid) {
  const el = document.getElementById("sessionIdDisplay");
  if (el) el.textContent = sid;
}

function appendMessageToHistory(role, text, ts = null) {
  const historyDiv = document.getElementById("chatHistory");
  const wrapper = document.createElement("div");
  wrapper.className = role === "assistant" ? "msg assistant" : "msg user";
  const meta = document.createElement("div");
  meta.className = "meta";
  const label = role === "assistant" ? "AI" : "You";
  const time = ts ? new Date(ts).toLocaleTimeString() : new Date().toLocaleTimeString();
  meta.textContent = `${label} • ${time}`;
  const content = document.createElement("div");
  content.className = "content";
  content.textContent = text;
  wrapper.appendChild(meta);
  wrapper.appendChild(content);
  historyDiv.appendChild(wrapper);
  historyDiv.scrollTop = historyDiv.scrollHeight;
}

async function fetchHistory(sid) {
  try {
    // const res = await fetch(`/agent/history/${encodeURIComponent(sid)}`);
    const json = await res.json();
    if (json && json.history) {
      const h = json.history;
      document.getElementById("chatHistory").innerHTML = "";
      for (const item of h) {
        appendMessageToHistory(item.role === "assistant" ? "assistant" : "user", item.content, item.ts);
      }
    }
  } catch (e) {
    console.warn("Could not fetch history:", e);
  }
}

window.addEventListener("load", () => {
  sessionId = getOrCreateSessionId();
  setSessionDisplay(sessionId);
  fetchHistory(sessionId);

  const aiAudio = document.getElementById("aiAudio");
  aiAudio.addEventListener("ended", () => {
    setTimeout(() => {
      startRecording();
    }, 300);
  });

  document.getElementById("startBtn").addEventListener("click", () => startRecording());
  document.getElementById("stopBtn").addEventListener("click", () => stopRecording());
});

function startRecording() {
  recordedChunks = [];
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };
    mediaRecorder.onstop = processAgentChat;
    mediaRecorder.start();
    document.getElementById("recordStatus").textContent = "🎙️ Recording...";
  }).catch(err => {
    document.getElementById("recordStatus").textContent = "❌ mic error: " + err.message;
  });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    document.getElementById("recordStatus").textContent = "⏳ Processing...";
  }
}

function processAgentChat() {
  const blob = new Blob(recordedChunks, { type: 'audio/webm' });
  const formData = new FormData();
  formData.append("audio", blob, "user_input.webm");

  document.getElementById("recordStatus").textContent = "⏳ Transcribing & thinking...";

  fetch(`/agent/chat/${encodeURIComponent(sessionId)}`, {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) throw new Error(data.error);

      // display user's recording
      const recordedAudio = document.getElementById("recordedAudio");
      recordedAudio.src = URL.createObjectURL(blob);
      recordedAudio.style.display = "block";

      // append transcript and assistant reply
      if (data.transcript) appendMessageToHistory("user", data.transcript);
      if (data.response_text) appendMessageToHistory("assistant", data.response_text);

      // play assistant audio
      if (data.audio_url) {
        const aiAudio = document.getElementById("aiAudio");
        aiAudio.src = data.audio_url;
        aiAudio.style.display = "block";
        aiAudio.play().catch(err => {
          console.warn("autoplay prevented:", err);
        });
      }

      document.getElementById("recordStatus").textContent = "✅ Response ready.";
    })
    .catch(err => {
  let fallbackMessage;
  
  // Check for API key failure keywords in the error
  if (err.message.includes("Unauthorized") || err.message.includes("401") || err.message.includes("Invalid API key")) {
    fallbackMessage = "⚠️ The AI service is unavailable. Please check your API key or try again later.";
  } else {
    fallbackMessage = "❌ Error: " + err.message;
  }

  // Show on UI
  document.getElementById("recordStatus").textContent = fallbackMessage;

  // Optionally also show in chat history
  appendMessageToHistory("assistant", fallbackMessage);

  console.error(err);
});

}
