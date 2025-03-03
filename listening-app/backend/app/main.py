import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router
from app.db.database import Base, async_engine
from app.config import API_TITLE, API_DESCRIPTION, API_VERSION, AUDIO_DIR

# Create tables in the database using lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables before startup
    from app.db.models import Exercise, Question, Option
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Cleanup operations could go here

# Initialize FastAPI application with lifespan
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
os.makedirs(os.path.join(os.path.dirname(__file__), "../static"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "../static/audio"), exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../static")), name="static")

# Include routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Listening Learning App"}

# Entry point to run with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)