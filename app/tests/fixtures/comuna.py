import pytest
from app.dependencies.testing_database import override_get_db

from app.models.comuna import ComunaModel
from app.schemas.comuna import ComunaCreate


@pytest.fixture
def comunas(db_engine):
    db = next(override_get_db())
    comuna = ComunaModel(**ComunaCreate(nombre="Comuna 1", codigo="COD_001").dict())
    if not db.query(ComunaModel).filter(ComunaModel.codigo == comuna.codigo).first():
        db.add(comuna)
        db.commit()
        db.refresh(comuna)
        #db.close()
