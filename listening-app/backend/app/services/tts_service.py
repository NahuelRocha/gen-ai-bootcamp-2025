import os
import uuid
import torch
import numpy as np
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from scipy.io.wavfile import write as write_wav
from app.config import AUDIO_DIR

class TTSService:
    def __init__(self, reference_audio_path: str = None):
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        # Si se dispone de un audio de referencia, se intenta obtener un embedding más real.
        if reference_audio_path and os.path.exists(reference_audio_path):
            import torchaudio
            waveform, sr = torchaudio.load(reference_audio_path)
            # (Esta es una aproximación; en la práctica deberías usar un método adecuado para extraer el embedding)
            embedding = torch.mean(waveform, dim=1, keepdim=True).unsqueeze(0)
            # Ajustar al tamaño requerido (1, 512) – aquí se trunca o se rellena
            if embedding.shape[-1] < 512:
                self.speaker_embeddings = torch.nn.functional.pad(embedding, (0, 512 - embedding.shape[-1]), "constant", 0)
            else:
                self.speaker_embeddings = embedding[:, :512]
        else:
            # Sin audio de referencia, se usa un vector fijo (esto puede dar voz menos natural)
            self.speaker_embeddings = torch.ones((1, 512))

    def preprocess_text(self, text: str) -> str:
        # Eliminar espacios y normalizar
        return " ".join(text.split())

    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        # Escala el audio para que el valor máximo sea 0.99
        max_val = np.abs(audio).max()
        if max_val > 0:
            audio = audio / max_val * 0.99
        return audio

    def insert_silence(self, duration_ms: int, sample_rate: int) -> np.ndarray:
        # Genera un segmento de silencio de 'duration_ms' milisegundos
        num_samples = int(sample_rate * duration_ms / 1000)
        return np.zeros(num_samples, dtype=np.float32)

    def split_text_into_chunks(self, text: str, max_length: int) -> list:
        """
        Divide el texto en fragmentos basados en oraciones.
        Acumula oraciones hasta acercarse al límite de tokens.
        """
        sentences = text.split(". ")
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if not sentence.endswith("."):
                sentence += "."
            candidate = (current_chunk + " " + sentence).strip() if current_chunk else sentence
            inputs = self.processor(text=candidate, return_tensors="pt")
            token_count = inputs["input_ids"].shape[1]
            if token_count <= max_length:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    async def generate_audio(self, text, language="en"):
        filename = f"{uuid.uuid4()}.wav"
        filepath = os.path.join(AUDIO_DIR, filename)
        try:
            processed_text = self.preprocess_text(text)
            max_length = 600  # Límite de tokens por fragmento

            # Si el texto completo cabe, no se segmenta
            inputs_full = self.processor(text=processed_text, return_tensors="pt")
            if inputs_full["input_ids"].shape[1] <= max_length:
                chunks = [processed_text]
            else:
                chunks = self.split_text_into_chunks(processed_text, max_length)
            
            audio_segments = []
            sample_rate = 16000
            for chunk in chunks:
                inputs = self.processor(text=chunk, return_tensors="pt")
                if inputs["input_ids"].shape[1] > max_length:
                    inputs["input_ids"] = inputs["input_ids"][:, :max_length]
                # Usar muestreo para mayor variabilidad en la entonación
                speech = self.model.generate_speech(
                    inputs["input_ids"],
                    self.speaker_embeddings,
                    vocoder=self.vocoder,
                )
                # Convertir a numpy y asegurar que sea 1D
                speech_np = speech.numpy()
                if speech_np.ndim > 1:
                    speech_np = speech_np.flatten()
                audio_segments.append(speech_np)
                # Insertar 200 ms de silencio entre fragmentos
                silence = self.insert_silence(200, sample_rate)
                audio_segments.append(silence)
            if audio_segments:
                audio_segments = audio_segments[:-1]  # Remover silencio final
            full_audio = np.concatenate(audio_segments, axis=0)
            full_audio = self.normalize_audio(full_audio)
            write_wav(filepath, sample_rate, full_audio)
            return filename
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return ""
