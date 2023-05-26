import pytest
import random
from faker import Faker
from enum import IntEnum

from app.db.connection import Base
from app.db.testing_connection import engine
from app.dependencies.testing_database import override_get_db

from app.models.comuna import ComunaModel
from app.schemas.comuna import ComunaCreate
from app.models.barrio import BarrioModel
from app.schemas.barrio import BarrioCreate
from app.models.vereda import VeredaModel
from app.schemas.vereda import VeredaCreate
from app.models.sector import SectorModel
from app.schemas.sector import SectorCreate
from app.models.areaexp import AreaExpModel
from app.schemas.areaexp import AreaExpCreate
from app.models.areapro import AreaProModel
from app.schemas.areapro import AreaProCreate
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraCreate

fake = Faker()
fake.seed_instance('tangara-mvp')


# IDs Lugares
class Codes(IntEnum):
    COMUNA = 1000
    BARRIO = 2000
    VEREDA = 3000
    SECTOR = 4000
    AREAEXP = 5000
    AREAPRO = 6000


# Totals
class Totals(IntEnum):
    COMUNAS = 7
    BARRIOS = 21
    VEREDAS = 5
    SECTORES = 12
    AREASEXP = 8
    AREASPRO = 3
    TANGARAS = 25


@pytest.fixture
def db_engine():
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def comunas(db_engine):
    db = next(override_get_db())
    for id_comuna in range(Codes.COMUNA, Codes.COMUNA + Totals.COMUNAS):
        comuna = ComunaModel(**ComunaCreate(
            id=id_comuna,
            nombre=f"Comuna {fake.unique.bothify(text='###')}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}").dict()
        )
        if not db.query(ComunaModel).filter(ComunaModel.codigo == comuna.codigo or ComunaModel.id == comuna.id).first():
            db.add(comuna)
            db.commit()


@pytest.fixture
def barrios(db_engine, comunas):
    db = next(override_get_db())
    for id_barrio in range(Codes.BARRIO, Codes.BARRIO + Totals.BARRIOS):
        id_comuna = random.choice(range(
            Codes.COMUNA,
            Codes.COMUNA + Totals.COMUNAS)
        )
        barrio = BarrioModel(**BarrioCreate(
            id=id_barrio,
            id_comuna=id_comuna,
            nombre=f"Barrio {fake.unique.street_name()}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}",
            estrato=f"{fake.random_int(min=0, max=9)}").dict()
        )
        if not db.query(BarrioModel).filter(BarrioModel.codigo == barrio.codigo or BarrioModel.id == barrio.id).first():
            db.add(barrio)
            db.commit()


@pytest.fixture
def veredas(db_engine):
    db = next(override_get_db())
    for id_vereda in range(Codes.VEREDA, Codes.VEREDA + Totals.VEREDAS):
        vereda = VeredaModel(**VeredaCreate(
            id=id_vereda,
            nombre=f"Vereda {fake.unique.street_name()}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}").dict()
        )
        if not db.query(VeredaModel).filter(VeredaModel.codigo == vereda.codigo or VeredaModel.id == vereda.id).first():
            db.add(vereda)
            db.commit()


@pytest.fixture
def sectores(db_engine, veredas):
    db = next(override_get_db())
    for id_sector in range(Codes.SECTOR, Codes.SECTOR + Totals.SECTORES):
        id_vereda = random.choice(range(
            Codes.VEREDA,
            Codes.VEREDA + Totals.VEREDAS)
        )
        sector = SectorModel(**SectorCreate(
            id=id_sector,
            id_vereda=id_vereda,
            nombre=f"Sector {fake.unique.street_name()}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}").dict()
        )
        if not db.query(SectorModel).filter(SectorModel.codigo == sector.codigo or SectorModel.id == sector.id).first():
            db.add(sector)
            db.commit()


@pytest.fixture
def areasexp(db_engine):
    db = next(override_get_db())
    for id_areaexp in range(Codes.AREAEXP, Codes.AREAEXP + Totals.AREASEXP):
        areaexp = AreaExpModel(**AreaExpCreate(
            id=id_areaexp,
            nombre=f"AreaExp {fake.unique.street_name()}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}").dict()
        )
        if not db.query(AreaExpModel).filter(AreaExpModel.codigo == areaexp.codigo or AreaExpModel.id == areaexp.id).first():
            db.add(areaexp)
            db.commit()


@pytest.fixture
def areaspro(db_engine):
    db = next(override_get_db())
    for id_areapro in range(Codes.AREAPRO, Codes.AREAPRO + Totals.AREASPRO):
        areapro = AreaProModel(**AreaProCreate(
            id=id_areapro,
            nombre=f"AreaPro {fake.unique.street_name()}",
            codigo=f"{fake.unique.bothify(text='???_###').upper()}").dict()
        )
        if not db.query(AreaProModel).filter(AreaProModel.codigo == areapro.codigo or AreaProModel.id == areapro.id).first():
            db.add(areapro)
            db.commit()


@pytest.fixture
def tangaras(db_engine, barrios, sectores, areasexp, areaspro):
    db = next(override_get_db())
    for id_tangara in range(Totals.TANGARAS):
        lugar = random.choice(
            [Codes.BARRIO, Codes.SECTOR, Codes.AREAEXP, Codes.AREAPRO]
        )
        total = {Codes.BARRIO: Totals.BARRIOS, Codes.SECTOR: Totals.SECTORES,
                 Codes.AREAEXP: Totals.AREASEXP, Codes.AREAPRO: Totals.AREASPRO}
        id_lugar = random.choice(range(
            lugar,
            lugar + total[lugar])
        )
        mac = fake.unique.hexify(text='^^:^^:^^:^^:^^:^^', upper=True)
        dict_tangara = {
            "id": id_tangara,
            "mac": mac,
            "geohash": f"d29{fake.unique.bothify(text='?#?#')}",
            "codigo": f"TANGARA_{mac.split(':')[-2]}{mac.split(':')[-1]}",
            "latitud": fake.unique.latitude(),
            "longitud": fake.unique.longitude(),
            "online": fake.boolean()
        }
        match lugar:
            case Codes.BARRIO:
                dict_tangara['id_barrio'] = id_lugar
            case Codes.SECTOR:
                dict_tangara['id_sector'] = id_lugar
            case Codes.AREAEXP:
                dict_tangara['id_areaexp'] = id_lugar
            case Codes.AREAPRO:
                dict_tangara['id_areapro'] = id_lugar
            case _:
                pass
        tangara = TangaraModel(**TangaraCreate.validate(dict_tangara).dict())
        if not db.query(TangaraModel).filter(TangaraModel.codigo == tangara.codigo or TangaraModel.mac == tangara.mac or TangaraModel.id == tangara.id).first():
            db.add(tangara)
            db.commit()
