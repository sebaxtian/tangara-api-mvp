from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class TangaraModel(Base):
    __tablename__ = "tangara"

    id = Column(Integer, primary_key=True, index=True)
    mac = Column(String, nullable=False, unique=True)
    geohash = Column(String, nullable=False)
    codigo = Column(String, nullable=False, unique=True)
    latitud = Column(String, nullable=False)
    longitud = Column(String, nullable=False)
    online = Column(Boolean, nullable=False)
    created = Column(String, nullable=False)
    updated = Column(String, nullable=False)

    id_areaexp = Column(Integer, ForeignKey("areaexp.id"))
    id_areapro = Column(Integer, ForeignKey("areapro.id"))

    areaexp = relationship("AreaExpModel", back_populates="tangaras")
    areapro = relationship("AreaProModel", back_populates="tangaras")
