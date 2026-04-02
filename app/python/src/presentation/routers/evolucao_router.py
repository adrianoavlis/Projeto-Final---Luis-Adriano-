from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.gasto_mensal_repository_impl import SqlGastoMensalRepository
from ...application.dtos.evolucao_filtro import EvolucaoFiltro
from ...application.use_cases.listar_serie_municipio import ListarSerieMunicipioUseCase
from ...application.use_cases.calcular_indicadores import CalcularIndicadoresUseCase
from ...application.use_cases.calcular_peso_componentes import CalcularPesoComponentesUseCase
from ...domain.value_objects.year_month import YearMonth

router = APIRouter(prefix="/evolucao", tags=["Evolução"])


# ── Schemas de resposta ──────────────────────────────────────────────────────

class SerieItemResponse(BaseModel):
    mes: str
    cesta: float
    componentes: dict[str, float]


class SerieMunicipioResponse(BaseModel):
    municipio: str
    serie: list[SerieItemResponse]


class IndicadorPrecoResponse(BaseModel):
    valor: float
    municipio: str
    municipio_id: str
    mes: str
    mes_descricao: str
    observacao: str


class VariacaoResponse(BaseModel):
    percentual: Optional[float]
    descricao: str
    municipios_considerados: int


class TendenciaResponse(BaseModel):
    percentual: Optional[float]
    texto: str
    descricao: str
    status: str
    municipios_considerados: int


class IndicadoresResponse(BaseModel):
    menor_preco: Optional[IndicadorPrecoResponse]
    variacao_mensal: Optional[VariacaoResponse]
    variacao_anual: Optional[VariacaoResponse]
    tendencia: Optional[TendenciaResponse]


class ComponentePesoResponse(BaseModel):
    chave: str
    media: float
    percentual: float
    variacao: Optional[float]
    valor_inicial: Optional[float]
    valor_final: Optional[float]
    mes_inicial: Optional[str]
    mes_final: Optional[str]


class PesoDestaquesResponse(BaseModel):
    item_mais_caro: Optional[ComponentePesoResponse]
    item_mais_barato: Optional[ComponentePesoResponse]
    maior_aumento: Optional[ComponentePesoResponse]
    maior_reducao: Optional[ComponentePesoResponse]


class PesoMunicipioResponse(BaseModel):
    id: str
    nome: str
    uf: str
    rotulo: str
    periodo_inicio: Optional[str]
    periodo_fim: Optional[str]
    total_medio: float
    componentes: list[ComponentePesoResponse]
    destaques: Optional[PesoDestaquesResponse]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _parse_filtro(
    municipios: list[str],
    mes_inicio: Optional[str],
    mes_fim: Optional[str],
    ano_referencia: Optional[int],
) -> EvolucaoFiltro:
    return EvolucaoFiltro(
        municipios=municipios,
        mes_inicio=YearMonth.from_string(mes_inicio) if mes_inicio else None,
        mes_fim=YearMonth.from_string(mes_fim) if mes_fim else None,
        ano_referencia=ano_referencia,
    )


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/series", response_model=list[SerieMunicipioResponse])
def listar_series(
    municipios: list[str] = Query(default=[]),
    mes_inicio: Optional[str] = Query(default=None),
    mes_fim: Optional[str] = Query(default=None),
    ano_referencia: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    filtro = _parse_filtro(municipios, mes_inicio, mes_fim, ano_referencia)
    repo = SqlGastoMensalRepository(db)
    series = ListarSerieMunicipioUseCase(repo).executar(filtro)
    return [
        SerieMunicipioResponse(
            municipio=s.municipio,
            serie=[SerieItemResponse(mes=p.mes, cesta=p.cesta, componentes=p.componentes) for p in s.serie],
        )
        for s in series
    ]


@router.get("/indicadores", response_model=IndicadoresResponse)
def calcular_indicadores(
    municipios: list[str] = Query(default=[]),
    mes_inicio: Optional[str] = Query(default=None),
    mes_fim: Optional[str] = Query(default=None),
    ano_referencia: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    filtro = _parse_filtro(municipios, mes_inicio, mes_fim, ano_referencia)
    repo = SqlGastoMensalRepository(db)
    dto = CalcularIndicadoresUseCase(repo).executar(filtro)
    return IndicadoresResponse(
        menor_preco=IndicadorPrecoResponse(**vars(dto.menor_preco)) if dto.menor_preco else None,
        variacao_mensal=VariacaoResponse(**vars(dto.variacao_mensal)) if dto.variacao_mensal else None,
        variacao_anual=VariacaoResponse(**vars(dto.variacao_anual)) if dto.variacao_anual else None,
        tendencia=TendenciaResponse(**vars(dto.tendencia)) if dto.tendencia else None,
    )


def _comp_response(c) -> ComponentePesoResponse:
    return ComponentePesoResponse(
        chave=c.chave,
        media=c.media,
        percentual=c.percentual,
        variacao=c.variacao,
        valor_inicial=c.valor_inicial,
        valor_final=c.valor_final,
        mes_inicial=c.mes_inicial,
        mes_final=c.mes_final,
    )


@router.get("/peso-componentes", response_model=list[PesoMunicipioResponse])
def calcular_peso_componentes(
    municipios: list[str] = Query(default=[]),
    mes_inicio: Optional[str] = Query(default=None),
    mes_fim: Optional[str] = Query(default=None),
    ano_referencia: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    filtro = _parse_filtro(municipios, mes_inicio, mes_fim, ano_referencia)
    repo = SqlGastoMensalRepository(db)
    pesos = CalcularPesoComponentesUseCase(repo).executar(filtro)
    result = []
    for p in pesos:
        destaques = None
        if p.destaques:
            d = p.destaques
            destaques = PesoDestaquesResponse(
                item_mais_caro=_comp_response(d.item_mais_caro) if d.item_mais_caro else None,
                item_mais_barato=_comp_response(d.item_mais_barato) if d.item_mais_barato else None,
                maior_aumento=_comp_response(d.maior_aumento) if d.maior_aumento else None,
                maior_reducao=_comp_response(d.maior_reducao) if d.maior_reducao else None,
            )
        result.append(PesoMunicipioResponse(
            id=p.id,
            nome=p.nome,
            uf=p.uf,
            rotulo=p.rotulo,
            periodo_inicio=p.periodo_inicio,
            periodo_fim=p.periodo_fim,
            total_medio=p.total_medio,
            componentes=[_comp_response(c) for c in p.componentes],
            destaques=destaques,
        ))
    return result
