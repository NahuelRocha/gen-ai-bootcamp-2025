from fastapi import APIRouter, Depends, HTTPException, Body, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.services.dialogue_service import DialogueService
from app.services.audio_service import AudioService
import os

from app.db.database import get_db
from app.schemas.schemas import (
    Exercise, ExerciseCreate, ExerciseUpdate, ExerciseWithQuestions,
    ExerciseGenerationRequest, ExerciseResponse
)
from app.db.crud import (
    create_exercise, get_exercise, get_all_exercises,
    update_exercise, delete_exercise, get_questions_by_exercise,
    get_options_by_question
)
from app.config import AUDIO_DIR

router = APIRouter()
dialogue_service = DialogueService()
audio_service = AudioService()

# Ruta para generar un ejercicio completo
@router.post("/exercises/generate", response_model=ExerciseResponse)
async def generate_exercise(
    request: ExerciseGenerationRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        exercise = await dialogue_service.generate_and_persist_exercise(
            db,
            language=request.language,
            difficulty=request.difficulty,
            scenario=request.scenario,
            num_questions=request.num_questions
        )
        # Se retorna la respuesta completa, usando el modelo de respuesta adecuado.
        return {"exercise": exercise, "audio_url": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exercise: {str(e)}")

@router.post("/exercises/{exercise_id}/generate_audio", response_model=dict)
async def generate_exercise_audio(exercise_id: int, db: AsyncSession = Depends(get_db)):
    try:
        audio_filename = await audio_service.generate_audio_for_exercise(db, exercise_id)
        return {"audio_url": audio_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

# Ruta para obtener todos los ejercicios
@router.get("/exercises", response_model=List[Exercise])
async def read_exercises(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    exercises = await get_all_exercises(db, skip=skip, limit=limit)
    return exercises

# Ruta para obtener un ejercicio específico con sus preguntas y opciones
@router.get("/exercises/{exercise_id}", response_model=ExerciseWithQuestions)
async def read_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
):
    exercise = await get_exercise(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    # Obtener preguntas y opciones
    questions = await get_questions_by_exercise(db, exercise_id)
    
    # Construir la respuesta completa
    result = exercise.__dict__
    result["questions"] = []
    
    for question in questions:
        q_dict = question.__dict__
        q_dict["options"] = await get_options_by_question(db, question.id)
        result["questions"].append(q_dict)
    
    return result

# Ruta para crear un ejercicio manualmente
@router.post("/exercises", response_model=Exercise)
async def create_exercise_endpoint(
    exercise: ExerciseCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_exercise(db, exercise.dict())

# Ruta para actualizar un ejercicio
@router.put("/exercises/{exercise_id}", response_model=Exercise)
async def update_exercise_endpoint(
    exercise_id: int,
    exercise: ExerciseUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_exercise = await get_exercise(db, exercise_id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    return await update_exercise(db, exercise_id, exercise.dict(exclude_unset=True))

# Ruta para eliminar un ejercicio
@router.delete("/exercises/{exercise_id}")
async def delete_exercise_endpoint(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_exercise = await get_exercise(db, exercise_id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    return await delete_exercise(db, exercise_id)

# Ruta para obtener el audio de un ejercicio
@router.get("/exercises/{exercise_id}/audio")
async def get_exercise_audio(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
):
    exercise = await get_exercise(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    if not exercise.audio_path:
        raise HTTPException(status_code=404, detail="Audio no encontrado para este ejercicio")
    
    return {"audio_url": f"/static/audio/{exercise.audio_path}"}


@router.get("/exercises/{exercise_id}/audio-file")
async def get_exercise_audio_file(
    exercise_id: int,
    db: AsyncSession = Depends(get_db)
):
    exercise = await get_exercise(db, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    if not exercise.audio_path:
        raise HTTPException(status_code=404, detail="Audio no encontrado para este ejercicio")
    
    audio_path = os.path.join(AUDIO_DIR, exercise.audio_path)
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Archivo de audio no encontrado")
    
    return FileResponse(
        path=audio_path,
        media_type="audio/wav",
        filename=f"exercise_{exercise_id}.wav"
    )