from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Text,
    DateTime, UniqueConstraint, func,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class GastoMensalModel(Base):
    __tablename__ = "gastos_mensais"
    __table_args__ = (
        UniqueConstraint("municipio", "mes_ano", name="uk_gasto_municipio_mes"),
    )

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    municipio: str = Column(String(150), nullable=False)
    # armazenado como Date (primeiro dia do mês), igual ao conversor Java
    mes_ano: date = Column(Date, nullable=False)
    total_cesta: Decimal = Column(Numeric(10, 2), nullable=False)
    carne: Decimal | None = Column(Numeric(10, 2))
    leite: Decimal | None = Column(Numeric(10, 2))
    feijao: Decimal | None = Column(Numeric(10, 2))
    arroz: Decimal | None = Column(Numeric(10, 2))
    farinha: Decimal | None = Column(Numeric(10, 2))
    batata: Decimal | None = Column(Numeric(10, 2))
    tomate: Decimal | None = Column(Numeric(10, 2))
    pao: Decimal | None = Column(Numeric(10, 2))
    cafe: Decimal | None = Column(Numeric(10, 2))
    banana: Decimal | None = Column(Numeric(10, 2))
    acucar: Decimal | None = Column(Numeric(10, 2))
    oleo: Decimal | None = Column(Numeric(10, 2))
    manteiga: Decimal | None = Column(Numeric(10, 2))
    criado_em: datetime | None = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em: datetime | None = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class EventoExternoModel(Base):
    __tablename__ = "eventos_externos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(150), nullable=False)
    descricao: str | None = Column(Text)
    data_inicio: date = Column(Date, nullable=False)
    data_fim: date = Column(Date, nullable=False)
    impacto: str = Column(String(20), nullable=False)
    criado_em: datetime | None = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em: datetime | None = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
