FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .

RUN pip install numpy==1.26.4

# Instalar PyTorch con soporte CPU
RUN pip install --no-cache-dir \
    torch==2.2.1+cpu \
    torchaudio==2.2.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy TTS service code
COPY *.py .

EXPOSE 7067

CMD ["python", "tts_server.py"]