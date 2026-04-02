from __future__ import annotations
from decimal import Decimal
from unittest.mock import MagicMock
from src.domain.entities.gasto_mensal import GastoMensal
from src.domain.value_objects.year_month import YearMonth
from src.application.dtos.evolucao_filtro import EvolucaoFiltro
from src.application.use_cases.listar_serie_municipio import ListarSerieMunicipioUseCase


def _make_gasto(municipio: str, year: int, month: int, total: float) -> GastoMensal:
    g = GastoMensal(
        municipio=municipio,
        mes_ano=YearMonth(year, month),
        total_cesta=Decimal(str(total)),
    )
    return g


def test_serie_agrupa_por_municipio():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = [
        _make_gasto("São Paulo / SP", 2023, 1, 700.0),
        _make_gasto("São Paulo / SP", 2023, 2, 720.0),
        _make_gasto("Rio de Janeiro / RJ", 2023, 1, 680.0),
    ]
    uc = ListarSerieMunicipioUseCase(repo)
    filtro = EvolucaoFiltro()
    series = uc.executar(filtro)
    municipios = [s.municipio for s in series]
    assert len(series) == 2
    assert any("São Paulo" in m for m in municipios)
    assert any("Rio de Janeiro" in m for m in municipios)


def test_serie_filtro_municipio():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = [
        _make_gasto("São Paulo / SP", 2023, 1, 700.0),
        _make_gasto("Rio de Janeiro / RJ", 2023, 1, 680.0),
    ]
    uc = ListarSerieMunicipioUseCase(repo)
    filtro = EvolucaoFiltro(municipios=["SAO PAULO"])
    series = uc.executar(filtro)
    assert len(series) == 1
    assert "São Paulo" in series[0].municipio


def test_serie_ordenada_por_mes():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = [
        _make_gasto("Curitiba / PR", 2023, 3, 650.0),
        _make_gasto("Curitiba / PR", 2023, 1, 620.0),
        _make_gasto("Curitiba / PR", 2023, 2, 635.0),
    ]
    uc = ListarSerieMunicipioUseCase(repo)
    series = uc.executar(EvolucaoFiltro())
    assert len(series) == 1
    meses = [p.mes for p in series[0].serie]
    assert meses == ["Jan-2023", "Fev-2023", "Mar-2023"]


def test_serie_vazia_sem_municipios():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = []
    uc = ListarSerieMunicipioUseCase(repo)
    result = uc.executar(EvolucaoFiltro())
    assert result == []
