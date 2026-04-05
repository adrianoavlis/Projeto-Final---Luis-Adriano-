from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GastoMensalItemDTO:
    id: int | None
    municipio: str
    periodo: str          # MM/YYYY
    total_cesta: float
    carne: float | None = None
    leite: float | None = None
    feijao: float | None = None
    arroz: float | None = None
    farinha: float | None = None
    batata: float | None = None
    tomate: float | None = None
    pao: float | None = None
    cafe: float | None = None
    banana: float | None = None
    acucar: float | None = None
    oleo: float | None = None
    manteiga: float | None = None


@dataclass
class PaginaGastosDTO:
    itens: list[GastoMensalItemDTO]
    total: int
    pagina: int
    tamanho: int
    total_paginas: int


@dataclass
class ImportacaoMesDTO:
    periodo: str          # MM/YYYY
    inseridos: int = 0
    atualizados: int = 0
    erro: str | None = None


@dataclass
class ImportacaoResultadoDTO:
    total_processados: int = 0
    total_inseridos: int = 0
    total_atualizados: int = 0
    meses_sucesso: list[str] = field(default_factory=list)
    meses_erro: list[str] = field(default_factory=list)
    detalhes: list[ImportacaoMesDTO] = field(default_factory=list)
