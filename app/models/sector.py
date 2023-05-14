from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class Sector(Base):
    __tablename__ = "sector"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    created: Mapped[str] = mapped_column(nullable=False)
    updated: Mapped[str] = mapped_column(nullable=False)

    id_vereda: Mapped[int] = mapped_column(ForeignKey("vereda.id"))

    vereda: Mapped["Vereda"] = relationship(back_populates="sectores") # type: ignore
    tangaras: Mapped[List["Tangara"]] = relationship(back_populates="sector") # type: ignore
