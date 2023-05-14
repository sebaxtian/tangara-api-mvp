from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from schemas.comuna import ComunaCreate, Comuna as ComunaSchema
from crud.comuna import create_comuna
from database import SessionLocal, engine, Base

from models.barrio import Barrio
from models.comuna import Comuna
from models.tangara import Tangara
from models.vereda import Vereda
from models.sector import Sector
from models.areaexp import AreaExp
from models.areapro import AreaPro

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/comunas/", response_model=ComunaSchema)
def post_comuna(comuna: ComunaCreate, db: Session = Depends(get_db)):
    return create_comuna(db, comuna=comuna)
