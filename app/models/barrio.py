from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.dev import Base


class BarrioModel(Base):
    __tablename__ = "barrio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    estrato = Column(String, nullable=False)
    created = Column(String, nullable=False)
    updated = Column(String, nullable=False)

    id_comuna = Column(Integer, ForeignKey("comuna.id"))

    comuna = relationship("ComunaModel", back_populates="barrios")
    tangaras = relationship("TangaraModel", back_populates="barrio")
