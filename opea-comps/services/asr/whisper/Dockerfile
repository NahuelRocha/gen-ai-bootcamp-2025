FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Instalar PyTorch con soporte MKL para AMD
RUN pip install --no-cache-dir \
    torch==2.2.1+cpu \
    torchaudio==2.2.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Copy Whisper server code
COPY *.py .

# Download sample audio for testing
RUN curl -O https://github.com/intel/intel-extension-for-transformers/raw/main/intel_extension_for_transformers/neural_chat/assets/audio/sample.wav

EXPOSE 7066

CMD ["python", "whisper_server.py", "--device=cpu"]