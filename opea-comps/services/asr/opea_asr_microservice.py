import os
import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Whisper endpoint from environment variable
WHISPER_ENDPOINT = os.getenv("ASR_ENDPOINT", "http://localhost:7066")

@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Form(default="openai/whisper-small")
):
    # Forward the request to Whisper service
    files = {"file": (file.filename, file.file, file.content_type)}
    data = {"model": model}
    
    response = requests.post(
        f"{WHISPER_ENDPOINT}/v1/audio/transcriptions",
        files=files,
        data=data
    )
    
    return response.json()

@app.get("/health")
async def health_check():
    try:
        response = requests.get(f"{WHISPER_ENDPOINT}/health")
        if response.status_code == 200:
            return {"status": "healthy"}
    except:
        pass
    return {"status": "unhealthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9099)