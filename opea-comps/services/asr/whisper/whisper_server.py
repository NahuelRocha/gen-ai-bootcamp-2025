import os
import whisper
import uvicorn
import argparse
import torch
import psutil
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Optimizaciones de CPU
    torch.set_num_threads(4)  # Ajustar según número de cores disponibles
    torch.set_num_interop_threads(1)
    
    # Cargar modelo optimizado para CPU
    model = whisper.load_model("small", device="cpu")
    
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model_name: str = Form(default="openai/whisper-small")  # Agregamos para consistencia
):
    global model
    
    temp_file = f"temp_{file.filename}"
    try:
        # Validar extensión
        if not file.filename.lower().endswith(('.wav', '.mp3', '.flac')):
            return {"error": "Formato de audio no soportado"}, 400
        
        # Guardar archivo temporal
        with open(temp_file, "wb") as f:
            content = await file.read()
            if not content:
                return {"error": "Archivo vacío"}, 400
            f.write(content)
        
        # Transcribir con configuraciones optimizadas
        result = model.transcribe(
            temp_file,
            fp16=False,     # Deshabilitar fp16 ya que estamos en CPU
            language="es"   # Opcional: puedes especificar el idioma o dejarlo que lo detecte
        )
        
        return {"text": result["text"]}
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"error": f"Error procesando audio: {str(e)}"}, 500
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    memory = psutil.Process().memory_info()
    return {
        "memory_used_mb": memory.rss / 1024 / 1024,
        "cpu_percent": psutil.cpu_percent(),
        "cpu_threads": torch.get_num_threads()
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()
    
    uvicorn.run(app, host="0.0.0.0", port=7066)