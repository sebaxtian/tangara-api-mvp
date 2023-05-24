from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.dependencies.settings import get_settings

settings: Settings = get_settings()

db_sqlite = {"dev": "/db/tangara-mvp.db", "prod": ""}

SQLALCHEMY_DATABASE_URL = f"sqlite://{db_sqlite[settings.env]}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
class Base(DeclarativeBase):
    pass

Base.metadata.create_all(bind=engine)
