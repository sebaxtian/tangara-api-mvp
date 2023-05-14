from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class Barrio(Base):
    __tablename__ = "barrio"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    estrato: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[str] = mapped_column(nullable=False)
    updated: Mapped[str] = mapped_column(nullable=False)

    id_comuna: Mapped[int] = mapped_column(ForeignKey("comuna.id"))

    comuna: Mapped["Comuna"] = relationship(back_populates="barrios") # type: ignore
    tangaras:  Mapped[List["Tangara"]] = relationship(back_populates="barrio") # type: ignore
