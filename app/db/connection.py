from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.dependencies.settings import get_settings

settings: Settings = get_settings()

db_sqlite = {"dev": "tangara-mvp.db", "test": "test-tangara-mvp.db"}

SQLALCHEMY_DATABASE_URL = f"sqlite:///db/{db_sqlite[settings.env]}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
