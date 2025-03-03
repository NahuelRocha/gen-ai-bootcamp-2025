from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ============================
# Modelos Base (para compartir atributos comunes)
# ============================

# Base model para Option
class OptionBase(BaseModel):
    option_text: str  # Nombre correcto del campo

# Base model para Question
class QuestionBase(BaseModel):
    question_text: str  # Nombre correcto del campo

# Base model para Exercise
class ExerciseBase(BaseModel):
    title: str
    description: str
    scenario: str
    language: str
    difficulty: str
    dialog: str
    audio_path: Optional[str] = None

# ============================
# Modelos de Creación (para entradas)
# ============================

class OptionCreate(OptionBase):
    question_id: int

class QuestionCreate(QuestionBase):
    exercise_id: int

class ExerciseCreate(ExerciseBase):
    pass

# ============================
# Modelos de Actualización (para entradas parciales)
# ============================

class OptionUpdate(BaseModel):
    option_text: Optional[str] = None
    is_correct: Optional[bool] = None

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None

class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    language: Optional[str] = None
    difficulty: Optional[str] = None
    dialog: Optional[str] = None
    audio_path: Optional[str] = None

# ============================
# Modelos de Lectura (Read models)
# Estos reflejan la estructura real de tus tablas en la BD.
# ============================

class Option(OptionBase):
    id: int
    question_id: int
    is_correct: int  # Se almacena como entero (0 o 1)

    class Config:
        orm_mode = True

class Question(QuestionBase):
    id: int
    exercise_id: int
    created_at: datetime
    options: List[Option] = []  # Relación precargada

    class Config:
        orm_mode = True

class Exercise(ExerciseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[Question] = []  # Relación precargada

    class Config:
        orm_mode = True

class ExerciseWithQuestions(Exercise):
    questions: List[Question] = []

# ============================
# Modelos de Request/Response para la API
# ============================

class ExerciseGenerationRequest(BaseModel):
    language: str
    difficulty: str
    scenario: str
    num_questions: int = 5
    

class ExerciseResponse(BaseModel):
    exercise: Exercise  # Donde Exercise es tu modelo de lectura
    audio_url: Optional[str] = None

    class Config:
        orm_mode = True
