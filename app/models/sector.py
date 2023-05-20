from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class SectorModel(Base):
    __tablename__ = "sector"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    created = Column(String, nullable=False)
    updated = Column(String, nullable=False)

    id_vereda = Column(Integer, ForeignKey("vereda.id"))

    vereda = relationship("VeredaModel", back_populates="sectores")
    tangaras = relationship("TangaraModel", back_populates="sector")
