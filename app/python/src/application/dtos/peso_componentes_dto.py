from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ComponentePesoDTO:
    chave: str
    media: float
    percentual: float
    variacao: float | None
    valor_inicial: float | None
    valor_final: float | None
    mes_inicial: str | None
    mes_final: str | None


@dataclass
class PesoDestaquesDTO:
    item_mais_caro: ComponentePesoDTO | None = None
    item_mais_barato: ComponentePesoDTO | None = None
    maior_aumento: ComponentePesoDTO | None = None
    maior_reducao: ComponentePesoDTO | None = None


@dataclass
class PesoMunicipioDTO:
    id: str
    nome: str
    uf: str
    rotulo: str
    periodo_inicio: str | None
    periodo_fim: str | None
    total_medio: float
    componentes: list[ComponentePesoDTO] = field(default_factory=list)
    destaques: PesoDestaquesDTO | None = None
