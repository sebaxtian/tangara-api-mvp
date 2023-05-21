from sqlalchemy.orm import Session

from schemas.lugares import LugaresSchema
from models.comuna import ComunaModel
from models.barrio import BarrioModel
from models.vereda import VeredaModel
from models.sector import SectorModel
from models.areaexp import AreaExpModel
from models.areapro import AreaProModel


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
