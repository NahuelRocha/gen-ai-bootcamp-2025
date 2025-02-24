FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instalar PyTorch y torchaudio para CPU (usando el índice de PyTorch)
RUN pip install --no-cache-dir torch==2.2.1+cpu torchaudio==2.2.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Copiar archivo de requerimientos e instalar dependencias (sin incluir torch)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del servicio (llm_server.py)
COPY llm_server.py .

EXPOSE 7070

# Iniciar el servicio usando uvicorn, referenciando "llm_server:app"
CMD ["uvicorn", "llm_server:app", "--host", "0.0.0.0", "--port", "7070"]