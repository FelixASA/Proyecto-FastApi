from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base

propiedad_propietario = Table(
    "propiedad_propietario_table",
    Base.metadata,
    Column("propietario_id", ForeignKey("propietarios_table.id"), primary_key=True),
    Column("propiedad_id", ForeignKey("propiedades_table.id"), primary_key=True),
)

class Arrendatario(Base):
    __tablename__ = 'arrendatarios_table'

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, unique=True, autoincrement="auto")
    rfc: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(16), nullable=False)
    apellido: Mapped[str] = mapped_column(String(16), nullable=False)

    propiedades: Mapped[list["Propiedad"]] = relationship(back_populates="arrendatario")

class Propiedad(Base):
    __tablename__ = 'propiedades_table'

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, unique=True, autoincrement="auto")
    clave_catastral: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(16), nullable=False)
    arrendatario_id: Mapped[int] = mapped_column(ForeignKey("arrendatarios_table.id"))

    arrendatario: Mapped["Arrendatario"] = relationship(back_populates="propiedades")
    propietarios: Mapped[list["Propietario"]] = relationship(secondary="propiedad_propietario_table", back_populates="propiedades_prop")


class Propietario(Base):
    __tablename__ = 'propietarios_table'

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, unique=True, autoincrement="auto")
    rfc: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(16), nullable=False)
    apellido: Mapped[str] = mapped_column(String(16), nullable=False)

    propiedades_prop: Mapped[list["Propiedad"]] = relationship(secondary="propiedad_propietario_table", back_populates="propietarios")

