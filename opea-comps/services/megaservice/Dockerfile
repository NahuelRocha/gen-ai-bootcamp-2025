FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del megaserivce
COPY megaservice.py .

EXPOSE 8000

CMD ["uvicorn", "megaservice:app", "--host", "0.0.0.0", "--port", "8000"]
