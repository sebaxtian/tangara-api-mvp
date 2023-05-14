from __future__ import annotations
from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class Vereda(Base):
    __tablename__ = "vereda"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, unique=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True)
    created: Mapped[str] = mapped_column(nullable=False)
    updated: Mapped[str] = mapped_column(nullable=False)

    sectores: Mapped[List["Sector"]] = relationship(back_populates="vereda") # type: ignore
