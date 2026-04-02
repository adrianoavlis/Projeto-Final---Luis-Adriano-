from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from ...domain.value_objects.impacto import Impacto


@dataclass
class EventoExternoDTO:
    id: int | None
    titulo: str
    descricao: str
    data_inicio: date
    data_fim: date
    impacto: Impacto
    periodo_inicio: str
    periodo_fim: str


@dataclass
class EventoExternoFormDTO:
    titulo: str
    descricao: str
    data_inicio: date
    data_fim: date
    impacto: Impacto
    id: int | None = None
