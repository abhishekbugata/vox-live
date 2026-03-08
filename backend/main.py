from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from gtts import gTTS
import os

app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- API KEY CONFIGURATION ---
# Replace with your actual key or set it as an environment variable
GROQ_KEY = os.environ.get("GROQ_API_KEY", "your-key-here")
client = Groq(api_key=GROQ_KEY)

class TextQuery(BaseModel):
    question: str

def get_log_context():
    """Reads the current live logs for AI context."""
    if os.path.exists("live_stream.log"):
        with open("live_stream.log", "r") as f:
            return "".join(f.readlines()[-30:])
    return "System stream initialized. No logs currently recorded."

@app.post("/ask_live_voice")
async def ask_live_voice(audio: UploadFile = File(...)):
    try:
        with open("temp_query.wav", "wb") as f:
            f.write(await audio.read())
        
        with open("temp_query.wav", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )
        
        context = get_log_context()
        prompt = f"Logs:\n{context}\n\nUser Question: {transcription.text}\n\nAnalyze professionally."
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        answer = completion.choices[0].message.content

        tts = gTTS(text=answer, lang='en')
        tts.save("response.mp3")

        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Backend Error: {str(e)}"}

@app.post("/ask_live_text")
async def ask_live_text(request: TextQuery):
    try:
        context = get_log_context()
        prompt = f"Logs:\n{context}\n\nUser Question: {request.question}\n\nAnalyze professionally."
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        answer = completion.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Backend Error: {str(e)}"}

@app.get("/get_audio")
async def get_audio():
    if os.path.exists("response.mp3"):
        return FileResponse("response.mp3")
    return {"error": "Audio file missing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)