from app.db.connection import SessionLocal, engine, Base

from app.models.comuna import ComunaModel
from app.models.barrio import BarrioModel
from app.models.vereda import VeredaModel
from app.models.sector import SectorModel
from app.models.areaexp import AreaExpModel
from app.models.areapro import AreaProModel
from app.models.tangara import TangaraModel

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
