from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class SerieDTO:
    mes: str
    cesta: float
    componentes: dict[str, float] = field(default_factory=dict)


@dataclass
class SerieMunicipioDTO:
    municipio: str
    serie: list[SerieDTO] = field(default_factory=list)


@dataclass
class EvolucaoMunicipioDTO:
    id: str
    nome: str
    uf: str
    serie: list[SerieDTO] = field(default_factory=list)


@dataclass
class PeriodosDisponiveisDTO:
    anos: list[int] = field(default_factory=list)
    meses: list[str] = field(default_factory=list)
    meses_por_ano: dict[int, list[str]] = field(default_factory=dict)
