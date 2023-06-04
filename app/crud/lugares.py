from sqlalchemy.orm import Session

from app.schemas.lugares import LugaresSchema
from app.models.comuna import ComunaModel
from app.models.barrio import BarrioModel
from app.models.vereda import VeredaModel
from app.models.sector import SectorModel
from app.models.areaexp import AreaExpModel
from app.models.areapro import AreaProModel


class LugaresCRUD():

    # Read

    def read_lugares(db: Session) -> list[LugaresSchema]:
        lugares = []
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(ComunaModel).all()])
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(BarrioModel).all()])
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(VeredaModel).all()])
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(SectorModel).all()])
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(AreaExpModel).all()])
        lugares.extend([{"id": comuna.id, "nombre": comuna.nombre} for comuna in db.query(AreaProModel).all()])
        return lugares
