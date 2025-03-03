from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os

from app.db.crud import (
    create_exercise, create_question, create_option,
    get_exercise
)
from app.schemas.schemas import Exercise, ExerciseCreate
from app.config import AUDIO_DIR
from services.llm_service import LLMService
from services.tts_service import TTSService

class ExerciseService:
    def __init__(self):
        self.llm_service = LLMService()  # Asegúrate de tener esto
        self.tts_service = TTSService()

    async def generate_complete_exercise(
        self,
        db: AsyncSession,
        language: str,
        difficulty: str,
        scenario: str,
        num_questions: int = 5
    ) -> Exercise:
        # Paso 1: Generar el diálogo con el LLM
        dialog_data = await self.llm_service.generate_dialog(
            language=language,
            difficulty=difficulty,
            scenario=scenario
        )
        
        # Paso 2: Crear el ejercicio CON los datos generados
        exercise_data = {
            "title": dialog_data["title"],  # Usar el título del LLM
            "description": dialog_data["description"],  # Descripción del LLM
            "language": language,
            "difficulty": difficulty,
            "scenario": scenario,
            "dialog": dialog_data["dialog"],  # Diálogo generado
            "audio_path": None  # Se actualizará después
        }
        
        # Crear el ejercicio en la base de datos
        exercise = await create_exercise(db, exercise_data)
        
        # Paso 3: Generar preguntas basadas en el diálogo
        questions_data = await self.llm_service.generate_questions(
            dialog=dialog_data["dialog"],
            language=language,
            num_questions=num_questions
        )
        
        # Paso 4: Crear preguntas y opciones
        for q_data in questions_data:
            question = await create_question(db, {
                "exercise_id": exercise.id,
                "question_text": q_data["question_text"]
            })
            
            for opt_data in q_data["options"]:
                await create_option(db, {
                    "question_id": question.id,
                    "option_text": opt_data["option_text"],
                    "is_correct": opt_data["is_correct"]
                })
        
        # Paso 5: Generar y actualizar audio (ejemplo simplificado)
        audio_filename = await self.tts_service.generate_audio(dialog_data["dialog"])
        await self._update_exercise_audio(db, exercise.id, audio_filename)
        
        return await get_exercise(db, exercise.id)
    
    async def _generate_questions_and_options(
        self,
        db: AsyncSession,
        exercise_id: int,
        scenario_text: str,
        num_questions: int
    ):
        """
        Generate questions and options for an exercise.
        """
        # This is a placeholder implementation
        for i in range(1, num_questions + 1):
            question_data = {
                "exercise_id": exercise_id,
                "text": f"Sample question {i} about the scenario",
                "order": i
            }
            
            # Create question asynchronously
            question = await create_question(db, question_data)
            
            # Create options for this question
            for j in range(1, 4):
                is_correct = (j == 1)  # First option is correct for this example
                option_data = {
                    "question_id": question.id,
                    "text": f"Sample option {j} for question {i}",
                    "is_correct": is_correct,
                    "order": j
                }
                
                # Create option asynchronously
                await create_option(db, option_data)
    
    async def _update_exercise_audio(
        self,
        db: AsyncSession,
        exercise_id: int,
        audio_filename: str
    ):
        """
        Update the exercise with the generated audio path.
        """
        # In this implementation, we're just updating the audio_path field
        # In a real implementation, you would generate the actual audio file
        exercise = await get_exercise(db, exercise_id)
        exercise.audio_path = audio_filename