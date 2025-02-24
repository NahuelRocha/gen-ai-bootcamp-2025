import os
import io
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from comps import (
    MicroService, 
    ServiceOrchestrator, 
    ServiceType
)

class AudioDoc(BaseModel):
    audio_data: bytes
    sample_rate: Optional[int] = None
    format: Optional[str] = "wav"

class TextDoc(BaseModel):
    text: str
    language: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de servicios
ASR_SERVICE_HOST = os.getenv("ASR_SERVICE_HOST", "asr-service")
ASR_SERVICE_PORT = int(os.getenv("ASR_SERVICE_PORT", 9099))
LLM_SERVICE_HOST = os.getenv("LLM_SERVICE_HOST", "llm-service")
LLM_SERVICE_PORT = int(os.getenv("LLM_SERVICE_PORT", 7070))
TTS_SERVICE_HOST = os.getenv("TTS_SERVICE_HOST", "tts-service")
TTS_SERVICE_PORT = int(os.getenv("TTS_SERVICE_PORT", 7067))

# Funciones que invocan los servicios remotos (sin decoradores)
async def process_audio(audio_data: AudioDoc) -> TextDoc:
    """Procesa el audio usando el servicio ASR"""
    try:
        files = {"file": ("audio.wav", audio_data.audio_data, "audio/wav")}
        data = {"model": "openai/whisper-small"}
        response = requests.post(
            f"http://{ASR_SERVICE_HOST}:{ASR_SERVICE_PORT}/v1/audio/transcriptions",
            files=files,
            data=data
        )
        response.raise_for_status()
        return TextDoc(text=response.json()["text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR service error: {str(e)}")

async def translate_text(text_data: TextDoc) -> TextDoc:
    """Traduce el texto usando el servicio LLM"""
    try:
        response = requests.post(
            f"http://{LLM_SERVICE_HOST}:{LLM_SERVICE_PORT}/v1/translate",
            json={"text": text_data.text}
        )
        response.raise_for_status()
        return TextDoc(text=response.json()["translated_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM service error: {str(e)}")

async def generate_speech(text_data: TextDoc) -> AudioDoc:
    """Genera audio a partir del texto usando el servicio TTS"""
    try:
        response = requests.post(
            f"http://{TTS_SERVICE_HOST}:{TTS_SERVICE_PORT}/v1/text/speech",
            json={"text": text_data.text}
        )
        response.raise_for_status()
        return AudioDoc(audio_data=response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS service error: {str(e)}")

# Configurar el orquestador
orchestrator = ServiceOrchestrator()

# Crear instancias de MicroService para los servicios remotos
asr_service = MicroService(
    name="asr",
    host=ASR_SERVICE_HOST,
    port=ASR_SERVICE_PORT,
    endpoint="/v1/audio/transcriptions",
    use_remote_service=True,
    service_type=ServiceType.ASR
)

llm_service = MicroService(
    name="llm",
    host=LLM_SERVICE_HOST,
    port=LLM_SERVICE_PORT,
    endpoint="/v1/translate",
    use_remote_service=True,
    service_type=ServiceType.LLM
)

tts_service = MicroService(
    name="tts",
    host=TTS_SERVICE_HOST,
    port=TTS_SERVICE_PORT,
    endpoint="/v1/text/speech",
    use_remote_service=True,
    service_type=ServiceType.TTS
)

# Configurar el flujo en el orquestador
orchestrator.add(asr_service).add(llm_service).add(tts_service)
orchestrator.flow_to(asr_service, llm_service)
orchestrator.flow_to(llm_service, tts_service)

@app.post("/v1/process_audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    """Endpoint principal que procesa el flujo completo"""
    try:
        # Crear AudioDoc con los datos del archivo
        audio_data = AudioDoc(audio_data=await file.read())
        
        # Procesar el audio usando los servicios remotos
        transcription = await process_audio(audio_data)
        translation = await translate_text(transcription)
        audio_response = await generate_speech(translation)
        
        # Retornar el audio generado
        return StreamingResponse(
            io.BytesIO(audio_response.audio_data),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=translated_audio.wav"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Endpoint de health check que muestra la configuración del orquestador"""
    return {
        "status": "healthy",
        "orchestrator": {
            "asr": str(asr_service),
            "llm": str(llm_service),
            "tts": str(tts_service),
            "flow": str(orchestrator)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
