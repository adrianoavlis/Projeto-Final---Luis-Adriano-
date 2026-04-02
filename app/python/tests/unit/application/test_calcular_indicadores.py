from __future__ import annotations
from decimal import Decimal
from unittest.mock import MagicMock
from src.domain.entities.gasto_mensal import GastoMensal
from src.domain.value_objects.year_month import YearMonth
from src.application.dtos.evolucao_filtro import EvolucaoFiltro
from src.application.use_cases.calcular_indicadores import CalcularIndicadoresUseCase


def _gasto(mun: str, year: int, month: int, total: float) -> GastoMensal:
    return GastoMensal(
        municipio=mun,
        mes_ano=YearMonth(year, month),
        total_cesta=Decimal(str(total)),
    )


def _repo_com(*gastos):
    repo = MagicMock()
    repo.listar_por_filtro.return_value = list(gastos)
    repo.buscar_menor_preco.return_value = min(gastos, key=lambda g: float(g.total_cesta))
    return repo


def test_indicadores_todos_none_sem_dados():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = []
    repo.buscar_menor_preco.return_value = None
    uc = CalcularIndicadoresUseCase(repo)
    dto = uc.executar(EvolucaoFiltro())
    assert dto.menor_preco is None
    assert dto.variacao_mensal is None
    assert dto.variacao_anual is None
    assert dto.tendencia is None


def test_variacao_mensal_calculada():
    repo = _repo_com(
        _gasto("Curitiba / PR", 2023, 1, 600.0),
        _gasto("Curitiba / PR", 2023, 2, 630.0),
    )
    uc = CalcularIndicadoresUseCase(repo)
    dto = uc.executar(EvolucaoFiltro())
    assert dto.variacao_mensal is not None
    assert abs(dto.variacao_mensal.percentual - 5.0) < 0.1


def test_tendencia_alta():
    gastos = [_gasto("Manaus / AM", 2023, m, 500 + m * 20) for m in range(1, 7)]
    repo = _repo_com(*gastos)
    uc = CalcularIndicadoresUseCase(repo)
    dto = uc.executar(EvolucaoFiltro())
    assert dto.tendencia is not None
    assert dto.tendencia.status == "ALTA"


def test_menor_preco_retornado():
    repo = _repo_com(
        _gasto("Salvador / BA", 2023, 1, 550.0),
        _gasto("Fortaleza / CE", 2023, 1, 490.0),
    )
    uc = CalcularIndicadoresUseCase(repo)
    dto = uc.executar(EvolucaoFiltro())
    assert dto.menor_preco is not None
    assert dto.menor_preco.valor == 490.0
