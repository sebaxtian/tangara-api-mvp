from sqlalchemy.orm import Session

from typing import List

from models.comuna import Comuna
from schemas.comuna import ComunaCreate, ComunaUpdate

# Create


def create_comuna(db: Session, comuna: ComunaCreate) -> Comuna:
    db_comuna = Comuna(nombre=comuna.nombre, codigo=comuna.codigo,
                       created=comuna.created, updated=comuna.updated)
    db.add(db_comuna)
    db.commit()
    db.refresh(db_comuna)
    return db_comuna

# Read


def get_comunas(db: Session, skip: int = 0, limit: int = 100) -> List[Comuna]:
    return db.query(Comuna).offset(skip).limit(limit).all()


def get_comuna(db: Session, id_comuna: int) -> Comuna | None:
    return db.query(Comuna).filter(Comuna.id == id_comuna).first()

# Update


def update_comuna(db: Session, comuna: ComunaUpdate, id_comuna: int) -> Comuna:
    db_comuna = Comuna(nombre=comuna.nombre,
                       codigo=comuna.codigo, updated=comuna.updated)
    db.query(Comuna).filter(Comuna.id == id_comuna).update(db_comuna)
    return db_comuna


# Delete

def delete_comuna(db: Session, id_comuna: int) -> None:
    db.query(Comuna).filter(Comuna.id == id_comuna).delete()
