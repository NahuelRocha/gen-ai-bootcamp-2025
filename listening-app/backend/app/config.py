import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones de la API
API_TITLE = "Listening Learning App API"
API_DESCRIPTION = "API para generar ejercicios de comprensión auditiva para aprendizaje de idiomas"
API_VERSION = "1.0.0"

# Configuraciones de la base de datos
DATABASE_URL = f"sqlite:///{BASE_DIR}/database/listening_app.db"

# Rutas para almacenamiento de archivos
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Configuración de idiomas disponibles
AVAILABLE_LANGUAGES = ["english", "spanish"]

# Configuración de niveles de dificultad
DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]

# Configuración para modelos locales
MODEL_CACHE_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)