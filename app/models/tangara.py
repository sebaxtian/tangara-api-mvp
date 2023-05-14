from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class Tangara(Base):
    __tablename__ = "tangara"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True, autoincrement=True)
    mac: Mapped[str] = mapped_column(nullable=False, unique=True)
    geohash: Mapped[str] = mapped_column(nullable=False, unique=True)
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    latitud: Mapped[str] = mapped_column(nullable=False, unique=True)
    longitud: Mapped[str] = mapped_column(nullable=False, unique=True)
    online: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[str] = mapped_column(nullable=False)
    updated: Mapped[str] = mapped_column(nullable=False)

    id_barrio: Mapped[int | None] = mapped_column(ForeignKey("barrio.id"))
    id_sector: Mapped[int | None] = mapped_column(ForeignKey("sector.id"))
    id_areaexp: Mapped[int | None] = mapped_column(ForeignKey("areaexp.id"))
    id_areapro: Mapped[int | None] = mapped_column(ForeignKey("areapro.id"))

    barrio: Mapped["Barrio"] = relationship(back_populates="tangaras") # type: ignore
    sector: Mapped["Sector"] = relationship(back_populates="tangaras") # type: ignore
    areaexp: Mapped["AreaExp"] = relationship(back_populates="tangaras") # type: ignore
    areapro: Mapped["AreaPro"] = relationship(back_populates="tangaras") # type: ignore
