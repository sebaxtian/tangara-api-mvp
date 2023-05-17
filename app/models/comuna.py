from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ComunaModel(Base):
    __tablename__ = "comuna"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    created = Column(String, nullable=False)
    updated = Column(String, nullable=False)

    barrios = relationship("BarrioModel", back_populates="comuna")
