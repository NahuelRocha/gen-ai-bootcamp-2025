import asyncio
from app.services.llm_service import LLMService
from app.db.crud import create_exercise, create_question, create_option, get_exercise

class DialogueService:
    def __init__(self):
        self.llm_service = LLMService()

    async def generate_and_persist_exercise(self, db, language, difficulty, scenario, num_questions):
        # Generar diálogo, título y descripción
        dialog_data = await self.llm_service.generate_dialog(language, difficulty, scenario)
        exercise_data = {
            "title": dialog_data["title"],
            "description": dialog_data["description"],
            "language": language,
            "difficulty": difficulty,
            "scenario": scenario,
            "dialog": dialog_data["dialog"],
            "audio_path": None
        }
        exercise = await create_exercise(db, exercise_data)
        # Generar preguntas basadas en el diálogo
        questions_data = await self.llm_service.generate_questions(dialog_data["dialog"], language, num_questions)
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
        return await get_exercise(db, exercise.id)