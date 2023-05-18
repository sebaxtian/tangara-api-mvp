from database import SessionLocal, engine, Base

from models.comuna import ComunaModel
from models.barrio import BarrioModel

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
