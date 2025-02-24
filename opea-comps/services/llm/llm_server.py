import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Definición del modelo de request
class TranslationRequest(BaseModel):
    text: str

app = FastAPI()

# Permitir CORS (como en el servicio TTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el pipeline de traducción (modelo ligero para CPU)
try:
    translator = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
    print("Modelo de traducción cargado correctamente.")
except Exception as e:
    print(f"Error cargando el modelo de traducción: {e}")
    raise

@app.post("/v1/translate")
async def translate_text(request: TranslationRequest):
    try:
        input_text = request.text
        # Se asume que el modelo realiza una traducción literal sin enriquecimiento.
        result = translator(input_text, max_length=512)
        # El resultado es una lista de diccionarios; extraemos el texto traducido.
        translation = result[0]['translation_text'].strip()
        return {"translated_text": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7070)
