from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker


from app.config import DATABASE_URL

# Crear motor de base de datos síncrono (para migraciones)
engine = create_engine(
    DATABASE_URL.replace("sqlite:///", "sqlite:///"),
    connect_args={"check_same_thread": False}
)

# Crear motor de base de datos asíncrono (para operaciones de la aplicación)
async_engine = create_async_engine(
    DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
    connect_args={"check_same_thread": False}
)

# Sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Base declarativa para modelos ORM
Base = declarative_base()

# Función para obtener una sesión de base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit solo al final exitoso
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  # Cierra la sesión explícitamente