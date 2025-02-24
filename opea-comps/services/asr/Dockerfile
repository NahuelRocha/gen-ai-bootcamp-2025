FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ASR service code
COPY opea_asr_microservice.py .
COPY check_asr_server.py .

EXPOSE 9099

CMD ["python", "opea_asr_microservice.py"]