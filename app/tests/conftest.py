import pytest
import random
from faker import Faker
from enum import IntEnum
import pandas as pd
from fastapi.encoders import jsonable_encoder

from app.db.connection import Base
from app.db.testing_connection import engine
from app.dependencies.testing_database import override_get_db
from app.dependencies.tangara_cache import create_mem_cache

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
    TANGARAS = 100


@pytest.fixture
def men_cache():
    create_mem_cache()


@pytest.fixture
def db_engine(men_cache):
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


def _update_tangara(db, sensor, id_tangara, lugar, id_lugar):
    tangara = TangaraModel(**TangaraCreate.validate({
        "id": id_tangara,
        "mac": sensor["mac"],
        "geohash": sensor["geohash"],
        "codigo": sensor["codigo"],
        "latitud": sensor["latitud"],
        "longitud": sensor["longitud"],
        "online": fake.boolean()
    }).dict())
    match lugar:
        case Codes.BARRIO:
            tangara.id_barrio = id_lugar
        case Codes.SECTOR:
            tangara.id_sector = id_lugar
        case Codes.AREAEXP:
            tangara.id_areaexp = id_lugar
        case Codes.AREAPRO:
            tangara.id_areapro = id_lugar
        case _:
            pass
    if db.query(TangaraModel).filter(TangaraModel.codigo == tangara.codigo or TangaraModel.mac == tangara.mac).first():
        tangara.mac = fake.unique.hexify(text='^^:^^:^^:^^:^^:^^', upper=True)
        tangara.codigo = f"TANGARA_{tangara.mac.split(':')[-2]}{tangara.mac.split(':')[-1]}"
    #TODO: Refactoring, sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: tangara.codigo
    db.query(TangaraModel).filter(TangaraModel.id == id_tangara).update(jsonable_encoder(tangara))
    db.commit()

    return tangara


@pytest.fixture
def pm25(db_engine, tangaras):
    db = next(override_get_db())

    # Create 2 Comunas
    ids_comunas = [comuna.id for comuna in db.query(ComunaModel).offset(0).limit(2).all()]
    
    #print("Comunas:", len(ids_comunas), ids_comunas)

    # Create 5 Barrios
    ids_barrios = []
    for barrio in db.query(BarrioModel).offset(0).limit(5).all():
        barrio.id_comuna = ids_comunas[0] if barrio.id % 2 == 0 else ids_comunas[1]
        db.query(BarrioModel).filter(BarrioModel.id == barrio.id).update(jsonable_encoder(barrio))
        db.commit()
        ids_barrios.append(barrio.id)
    
    #print("Barrios:", len(ids_barrios), ids_barrios)

    # Create 2 Veredas
    ids_veredas = [vereda.id for vereda in db.query(VeredaModel).offset(0).limit(2).all()]

    #print("Veredas:", len(ids_veredas), ids_veredas)

    # Create 5 Sectores
    ids_sectores = []
    for sector in db.query(SectorModel).offset(0).limit(5).all():
        sector.id_vereda = ids_veredas[0] if sector.id % 2 == 0 else ids_veredas[1]
        db.query(SectorModel).filter(SectorModel.id == sector.id).update(jsonable_encoder(sector))
        db.commit()
        ids_sectores.append(sector.id)
    
    #print("Sectores:", len(ids_sectores), ids_sectores)

    # Create 3 AreasExp
    ids_areasexp = [areaexp.id for areaexp in db.query(AreaExpModel).offset(0).limit(3).all()]

    #print("AreasExp:", len(ids_areasexp), ids_areasexp)

    # Create 2 AreasPro
    ids_areaspro = [areapro.id for areapro in db.query(AreaProModel).offset(0).limit(2).all()]

    #print("AreasPro:", len(ids_areaspro), ids_areaspro)

    # Create 34 Tangaras
    sensors = pd.read_csv("db/csv/tangara.csv")
    sample_34 = sensors.sample(34, replace=True)
    sample_tangara = random.sample(range(0, Totals.TANGARAS), 34)
    ids_tangaras = []
    index = 0
    
    # 2 Comunas, 5 Barrios -> 15 Tangaras
    # Comuna 0, Barrio 0 -> 4 Tangara
    for _, sensor in sample_34.iloc[0:4].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.BARRIO, id_lugar=ids_barrios[0])
        ids_tangaras.append(tangara.id)
        index += 1
    # Comuna 1, Barrio 1 -> 1 Tangaras
    tangara = _update_tangara(db=db, sensor=sample_34.iloc[4], id_tangara=sample_tangara[index], lugar=Codes.BARRIO, id_lugar=ids_barrios[1])
    ids_tangaras.append(tangara.id)
    index += 1
    # Comuna 0, Barrio 2 -> 2 Tangaras
    for _, sensor in sample_34.iloc[5:7].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.BARRIO, id_lugar=ids_barrios[2])
        ids_tangaras.append(tangara.id)
        index += 1
    # Comuna 1, Barrio 3 -> 3 Tangara
    for _, sensor in sample_34.iloc[7:10].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.BARRIO, id_lugar=ids_barrios[3])
        ids_tangaras.append(tangara.id)
        index += 1
    # Comuna 0, Barrio 4 -> 5 Tangaras
    for _, sensor in sample_34.iloc[10:15].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.BARRIO, id_lugar=ids_barrios[4])
        ids_tangaras.append(tangara.id)
        index += 1
    

    # 2 Veredas, 5 Sectores -> 9 Tangaras
    # Vereda 0, Sector 0 -> 2 Tangara
    for _, sensor in sample_34.iloc[15:17].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.SECTOR, id_lugar=ids_sectores[0])
        ids_tangaras.append(tangara.id)
        index += 1
    # Vereda 1, Sector 1 -> 1 Tangaras
    tangara = _update_tangara(db=db, sensor=sample_34.iloc[17], id_tangara=sample_tangara[index], lugar=Codes.SECTOR, id_lugar=ids_sectores[1])
    ids_tangaras.append(tangara.id)
    index += 1
    # Vereda 0, Sector 2 -> 3 Tangaras
    for _, sensor in sample_34.iloc[18:21].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.SECTOR, id_lugar=ids_sectores[2])
        ids_tangaras.append(tangara.id)
        index += 1
    # Vereda 1, Sector 3 -> 1 Tangara
    tangara = _update_tangara(db=db, sensor=sample_34.iloc[21], id_tangara=sample_tangara[index], lugar=Codes.SECTOR, id_lugar=ids_sectores[3])
    ids_tangaras.append(tangara.id)
    index += 1
    # Vereda 0, Sector 4 -> 2 Tangaras
    for _, sensor in sample_34.iloc[22:24].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.SECTOR, id_lugar=ids_sectores[4])
        ids_tangaras.append(tangara.id)
        index += 1


    # 3 AreasExp -> 6 Tangaras
    # AreaExp 0 -> 1 Tangara
    tangara = _update_tangara(db=db, sensor=sample_34.iloc[24], id_tangara=sample_tangara[index], lugar=Codes.AREAEXP, id_lugar=ids_areasexp[0])
    ids_tangaras.append(tangara.id)
    index += 1
    # AreaExp 1 -> 3 Tangara
    for _, sensor in sample_34.iloc[25:28].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.AREAEXP, id_lugar=ids_areasexp[1])
        ids_tangaras.append(tangara.id)
        index += 1
    # AreaExp 2 -> 2 Tangara
    for _, sensor in sample_34.iloc[28:30].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.AREAEXP, id_lugar=ids_areasexp[2])
        ids_tangaras.append(tangara.id)
        index += 1


    # 2 AreasPro -> 4 Tangaras
    # AreaPro 0 -> 3 Tangara
    for _, sensor in sample_34.iloc[30:33].iterrows():
        tangara = _update_tangara(db=db, sensor=sensor, id_tangara=sample_tangara[index], lugar=Codes.AREAPRO, id_lugar=ids_areaspro[0])
        ids_tangaras.append(tangara.id)
        index += 1
    # AreaPro 1 -> 1 Tangara
    tangara = _update_tangara(db=db, sensor=sample_34.iloc[33], id_tangara=sample_tangara[index], lugar=Codes.AREAPRO, id_lugar=ids_areaspro[1])
    ids_tangaras.append(tangara.id)
    index += 1

    #print("ids_tangaras:", len(ids_tangaras), ids_tangaras)
