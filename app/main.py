from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


from schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate
from models.comuna import ComunaModel
from models.barrio import BarrioModel
from crud.comuna import ComunaCRUD
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/comunas/", response_model=list[ComunaSchema])
async def comunas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[ComunaSchema]:
    comunas = ComunaCRUD.read_comunas(db, skip=skip, limit=limit)
    return comunas


@app.get("/comuna/{id}", response_model=ComunaSchema)
async def comuna(id: int, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.read_comuna(db, id_comuna=id)
    return comuna


@app.post("/comuna/", response_model=ComunaSchema)
async def comuna(comuna: ComunaCreate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.create_comuna(db, comuna=comuna)
    return comuna


@app.put("/comuna/{id}", response_model=ComunaSchema)
async def comuna(id: int, comuna: ComunaUpdate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.update_comuna(db, id_comuna=id, comuna=comuna)
    return comuna


@app.delete("/comuna/{id}", response_model=None)
async def comuna(id: int, db: Session = Depends(get_db)) -> None:
    ComunaCRUD.delete_comuna(db, id_comuna=id)
