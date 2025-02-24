import io
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TTS_ENDPOINT = os.getenv("TTS_ENDPOINT", "http://localhost:7067")

class TextRequest(BaseModel):
    text: str

@app.post("/v1/text/speech")
async def convert_text_to_speech(request: TextRequest):
    try:
        response = requests.post(
            f"{TTS_ENDPOINT}/v1/text/speech",
            json={"text": request.text}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
        # Verificar el contenido de la respuesta
        if len(response.content) == 0:
            raise HTTPException(status_code=500, detail="Received empty audio from TTS service")
            
        print(f"Received audio size: {len(response.content)} bytes")  # Logging
        
        return StreamingResponse(
            io.BytesIO(response.content),
            media_type="audio/wav"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with TTS service: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        response = requests.get(f"{TTS_ENDPOINT}/health")
        if response.status_code == 200:
            return {"status": "healthy"}
    except:
        pass
    return {"status": "unhealthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9098)