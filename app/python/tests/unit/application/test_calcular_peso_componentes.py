from __future__ import annotations
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from src.domain.entities.gasto_mensal import GastoMensal
from src.domain.value_objects.year_month import YearMonth
from src.application.dtos.evolucao_filtro import EvolucaoFiltro
from src.application.use_cases.calcular_peso_componentes import CalcularPesoComponentesUseCase


def _gasto(municipio: str, year: int, month: int, total: float, componentes: dict | None = None) -> GastoMensal:
    g = GastoMensal(
        municipio=municipio,
        mes_ano=YearMonth(year, month),
        total_cesta=Decimal(str(total)),
    )
    if componentes:
        for nome, valor in componentes.items():
            g.set_componente(nome, Decimal(str(valor)))
    return g


def _repo_com(*gastos):
    repo = MagicMock()
    repo.listar_por_filtro.return_value = list(gastos)
    return repo


def test_retorna_vazio_sem_dados():
    repo = MagicMock()
    repo.listar_por_filtro.return_value = []
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert resultado == []


def test_agrupa_por_municipio():
    repo = _repo_com(
        _gasto("São Paulo / SP", 2023, 1, 600.0, {"carne": 80.0, "leite": 40.0}),
        _gasto("Curitiba / PR", 2023, 1, 550.0, {"carne": 70.0, "leite": 35.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert len(resultado) == 2
    ids = {r.id for r in resultado}
    assert "SAO PAULO" in ids
    assert "CURITIBA" in ids


def test_calcula_media_componente():
    repo = _repo_com(
        _gasto("Curitiba / PR", 2023, 1, 600.0, {"carne": 80.0}),
        _gasto("Curitiba / PR", 2023, 2, 620.0, {"carne": 100.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert len(resultado) == 1
    carne = next(c for c in resultado[0].componentes if c.chave == "carne")
    assert carne.media == 90.0


def test_calcula_percentual_componente():
    repo = _repo_com(
        _gasto("Curitiba / PR", 2023, 1, 200.0, {"carne": 100.0, "leite": 100.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    componentes = {c.chave: c for c in resultado[0].componentes}
    assert componentes["carne"].percentual == 50.0
    assert componentes["leite"].percentual == 50.0


def test_calcula_variacao_entre_periodos():
    repo = _repo_com(
        _gasto("Manaus / AM", 2023, 1, 500.0, {"carne": 100.0}),
        _gasto("Manaus / AM", 2023, 6, 550.0, {"carne": 150.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    carne = next(c for c in resultado[0].componentes if c.chave == "carne")
    assert carne.variacao == 50.0


def test_variacao_none_com_apenas_um_periodo():
    repo = _repo_com(
        _gasto("Fortaleza / CE", 2023, 1, 500.0, {"carne": 100.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    carne = next(c for c in resultado[0].componentes if c.chave == "carne")
    assert carne.variacao is None


def test_destaques_identificados():
    repo = _repo_com(
        _gasto("Recife / PE", 2023, 1, 500.0, {"carne": 200.0, "leite": 50.0, "arroz": 100.0}),
        _gasto("Recife / PE", 2023, 2, 520.0, {"carne": 220.0, "leite": 45.0, "arroz": 110.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    destaques = resultado[0].destaques
    assert destaques is not None
    assert destaques.item_mais_caro.chave == "carne"
    assert destaques.item_mais_barato.chave == "leite"


def test_filtro_municipio_aplicado():
    repo = _repo_com(
        _gasto("Salvador / BA", 2023, 1, 600.0, {"carne": 80.0}),
        _gasto("Natal / RN", 2023, 1, 550.0, {"carne": 70.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    filtro = EvolucaoFiltro(municipios=["Salvador"])
    resultado = uc.executar(filtro)
    assert len(resultado) == 1
    assert resultado[0].id == "SALVADOR"


def test_municipio_sem_uf():
    repo = _repo_com(
        _gasto("Manaus", 2023, 1, 500.0, {"carne": 80.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert len(resultado) == 1
    assert resultado[0].uf == ""
    assert resultado[0].rotulo == "Manaus"


def test_total_medio_soma_medias_componentes():
    repo = _repo_com(
        _gasto("Belém / PA", 2023, 1, 300.0, {"carne": 100.0, "leite": 50.0, "arroz": 30.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert resultado[0].total_medio == 180.0


def test_periodo_inicio_fim_preenchidos():
    repo = _repo_com(
        _gasto("Goiânia / GO", 2023, 1, 500.0, {"carne": 80.0}),
        _gasto("Goiânia / GO", 2023, 6, 520.0, {"carne": 90.0}),
    )
    uc = CalcularPesoComponentesUseCase(repo)
    resultado = uc.executar(EvolucaoFiltro())
    assert resultado[0].periodo_inicio == "Jan-2023"
    assert resultado[0].periodo_fim == "Jun-2023"
