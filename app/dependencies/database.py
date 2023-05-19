from database import SessionLocal, engine, Base

from models.comuna import ComunaModel
from models.barrio import BarrioModel
from models.vereda import VeredaModel
from models.sector import SectorModel
from models.areaexp import AreaExpModel
from models.areapro import AreaProModel
from models.tangara import TangaraModel

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
