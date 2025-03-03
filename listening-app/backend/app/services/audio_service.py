from app.db.crud import get_exercise, update_exercise_audio  # Asegúrate de tener update_exercise_audio implementado
from app.services.tts_service import TTSService

class AudioService:
    def __init__(self):
        self.tts_service = TTSService()
    
    async def generate_audio_for_exercise(self, db, exercise_id):
        exercise = await get_exercise(db, exercise_id)
        text = exercise.dialog
        audio_filename = await self.tts_service.generate_audio(text)
        await update_exercise_audio(db, exercise_id, audio_filename)
        return audio_filename