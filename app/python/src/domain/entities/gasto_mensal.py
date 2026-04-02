from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from .base import BaseEntity
from ..value_objects.year_month import YearMonth

COMPONENTES: tuple[str, ...] = (
    "carne", "leite", "feijao", "arroz", "farinha",
    "batata", "tomate", "pao", "cafe", "banana",
    "acucar", "oleo", "manteiga",
)


@dataclass
class GastoMensal(BaseEntity):
    municipio: str = ""
    mes_ano: YearMonth | None = None
    total_cesta: Decimal | None = None
    carne: Decimal | None = None
    leite: Decimal | None = None
    feijao: Decimal | None = None
    arroz: Decimal | None = None
    farinha: Decimal | None = None
    batata: Decimal | None = None
    tomate: Decimal | None = None
    pao: Decimal | None = None
    cafe: Decimal | None = None
    banana: Decimal | None = None
    acucar: Decimal | None = None
    oleo: Decimal | None = None
    manteiga: Decimal | None = None

    def get_componente(self, nome: str) -> Decimal | None:
        return getattr(self, nome, None)

    def set_componente(self, nome: str, valor: Decimal | None) -> None:
        if nome in COMPONENTES or nome == "total_cesta":
            setattr(self, nome, valor)
