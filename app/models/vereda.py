from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.connection import Base


class VeredaModel(Base):
    __tablename__ = "vereda"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    created = Column(String, nullable=False)
    updated = Column(String, nullable=False)

    sectores = relationship("SectorModel", back_populates="vereda")
