"""
Database connection et session management.

Supporte PostgreSQL en production et SQLite en développement.
"""

import os
from dotenv import load_dotenv

# Charge .env en premier
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from backend.models import Base

# Configuration
USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost/ai_assistant" if USE_POSTGRES
    else "sqlite:///./data/ai_assistant.db"
)

# Force SQLite pool settings
pool_kwargs = {}
if "sqlite" in DB_URL:
    pool_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": NullPool
    }

# Engine
engine = create_engine(DB_URL, **pool_kwargs)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dépendance FastAPI pour obtenir une session DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crée les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database initialized ({DB_URL})")


def reset_db():
    """Réinitialise complètement la base (attention!)."""
    print("⚠ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    init_db()
    print("✓ Database reset")
