from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from app.db.models import Exercise, Question, Option

# Operaciones CRUD para Exercise
async def create_exercise(db: AsyncSession, exercise_data):
    new_exercise = Exercise(**exercise_data)
    db.add(new_exercise)
    await db.flush()  # En lugar de commit
    return new_exercise

async def get_exercise(db: AsyncSession, exercise_id: int):
    result = await db.execute(
        select(Exercise)
        .options(
            selectinload(Exercise.questions).selectinload(Question.options)
        )
        .filter(Exercise.id == exercise_id)
    )
    return result.scalars().first()

async def get_all_exercises(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Exercise)
        .options(
            selectinload(Exercise.questions).selectinload(Question.options)
        )
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_exercise(db: AsyncSession, exercise_id: int, exercise_data):
    await db.execute(
        update(Exercise)
        .where(Exercise.id == exercise_id)
        .values(**exercise_data)
    )
    await db.commit()
    return await get_exercise(db, exercise_id)

async def delete_exercise(db: AsyncSession, exercise_id: int):
    await db.execute(delete(Exercise).where(Exercise.id == exercise_id))
    await db.commit()
    return {"success": True}

# Operaciones CRUD para Question
async def create_question(db: AsyncSession, question_data):
    new_question = Question(**question_data)
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question

async def get_questions_by_exercise(db: AsyncSession, exercise_id: int):
    result = await db.execute(select(Question).filter(Question.exercise_id == exercise_id))
    return result.scalars().all()

# Operaciones CRUD para Option
async def create_option(db: AsyncSession, option_data):
    new_option = Option(**option_data)
    db.add(new_option)
    await db.commit()
    await db.refresh(new_option)
    return new_option

async def get_options_by_question(db: AsyncSession, question_id: int):
    result = await db.execute(select(Option).filter(Option.question_id == question_id))
    return result.scalars().all()

async def update_exercise_audio(db, exercise_id: int, audio_filename: str):
    await db.execute(
        update(Exercise)
        .where(Exercise.id == exercise_id)
        .values(audio_path=audio_filename)
    )
    await db.commit()
    return await get_exercise(db, exercise_id)