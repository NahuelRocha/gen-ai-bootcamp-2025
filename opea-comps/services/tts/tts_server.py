import torch
import torchaudio
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
from fastapi.responses import StreamingResponse

class TextToSpeechRequest(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelos
try:
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    
    # Cargar speaker embeddings (embeddings por defecto)
    speaker_embeddings = torch.randn(1, 512)
except Exception as e:
    print(f"Error loading models: {str(e)}")
    raise

@app.post("/v1/text/speech")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        print(f"Recibiendo texto: {request.text}")
        
        # Procesar texto
        inputs = processor(text=request.text, return_tensors="pt")
        print("Texto procesado correctamente")
        
        # Generar speech con speaker embeddings y ajustar la velocidad con length_scale
        speech = model.generate_speech(
            inputs["input_ids"],
            speaker_embeddings=speaker_embeddings,
            vocoder=vocoder,
            length_scale=1.1
        )
        print(f"Audio generado. Shape: {speech.shape}")
        
        # Convertir a bytes
        buffer = io.BytesIO()
        torchaudio.save(buffer, speech.unsqueeze(0), 16000, format="wav")
        buffer.seek(0)
        
        size = buffer.getbuffer().nbytes
        print(f"Tamaño del audio generado: {size} bytes")
        
        if size == 0:
            raise HTTPException(status_code=500, detail="Audio generado tiene 0 bytes")
            
        return StreamingResponse(
            buffer,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
    
    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7067)
