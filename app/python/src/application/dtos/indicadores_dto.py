from __future__ import annotations
from dataclasses import dataclass


@dataclass
class IndicadorPrecoDTO:
    valor: float
    municipio: str
    municipio_id: str
    mes: str
    mes_descricao: str
    observacao: str


@dataclass
class VariacaoDTO:
    percentual: float | None
    descricao: str
    municipios_considerados: int


@dataclass
class TendenciaDTO:
    percentual: float | None
    texto: str
    descricao: str
    status: str  # ALTA, QUEDA, ESTAVEL, INDEFINIDO
    municipios_considerados: int


@dataclass
class IndicadoresDTO:
    menor_preco: IndicadorPrecoDTO | None
    variacao_mensal: VariacaoDTO | None
    variacao_anual: VariacaoDTO | None
    tendencia: TendenciaDTO | None
