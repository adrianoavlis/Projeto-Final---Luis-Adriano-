from __future__ import annotations
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.models import GastoMensalModel
from src.domain.value_objects.year_month import YearMonth

from datetime import date


# ── Helpers ───────────────────────────────────────────────────────────────────

def _model(municipio: str, mes_ano: date, total: float, **componentes) -> GastoMensalModel:
    m = GastoMensalModel()
    m.id = None
    m.municipio = municipio
    m.mes_ano = mes_ano
    m.total_cesta = Decimal(str(total))
    for campo, valor in componentes.items():
        setattr(m, campo, Decimal(str(valor)))
    m.criado_em = None
    m.atualizado_em = None
    return m


def _fake_session(models: list, menor_preco_model=None):
    fake = MagicMock()

    # Resultado para queries que retornam lista (listar_por_filtro, listar_periodos)
    fake_scalars = MagicMock()
    fake_scalars.__iter__ = MagicMock(side_effect=lambda: iter(models))
    fake_scalars.all.return_value = [m.mes_ano for m in models]
    fake_list_result = MagicMock()
    fake_list_result.scalars.return_value = fake_scalars

    # buscar_menor_preco faz 2 execute():
    #   1º → scalar_one_or_none() retorna string (nome do município)
    #   2º → scalar_one_or_none() retorna GastoMensalModel
    best_mun = menor_preco_model.municipio if menor_preco_model else None
    fake_mun_result = MagicMock()
    fake_mun_result.scalar_one_or_none.return_value = best_mun
    fake_model_result = MagicMock()
    fake_model_result.scalar_one_or_none.return_value = menor_preco_model

    # execute() chamado em ordem: listar_por_filtro, depois buscar_menor_preco (x2)
    fake.execute.side_effect = [
        fake_list_result,     # listar_por_filtro
        fake_mun_result,      # buscar_menor_preco: subquery municipio
        fake_model_result,    # buscar_menor_preco: model completo
    ]
    return fake


@pytest.fixture
def client_gastos():
    models = [
        _model("São Paulo / SP", date(2023, 1, 1), 620.0, carne=85.0, leite=42.0),
        _model("São Paulo / SP", date(2023, 2, 1), 640.0, carne=90.0, leite=44.0),
        _model("Curitiba / PR", date(2023, 1, 1), 580.0, carne=75.0, leite=38.0),
    ]
    menor = _model("Curitiba / PR", date(2023, 1, 1), 580.0, carne=75.0, leite=38.0)
    fake = _fake_session(models, menor_preco_model=menor)
    app.dependency_overrides[get_db] = lambda: fake
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_sem_dados():
    fake = _fake_session([])
    app.dependency_overrides[get_db] = lambda: fake
    yield TestClient(app)
    app.dependency_overrides.clear()


# ── /api/municipios ───────────────────────────────────────────────────────────

def test_listar_municipios_200(client_gastos):
    response = client_gastos.get("/api/municipios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "Curitiba / PR" in data
    assert "São Paulo / SP" in data


def test_listar_municipios_sem_dados_retorna_lista_vazia(client_sem_dados):
    response = client_sem_dados.get("/api/municipios")
    assert response.status_code == 200
    assert response.json() == []


# ── /api/periodos ─────────────────────────────────────────────────────────────

def test_listar_periodos_200(client_gastos):
    response = client_gastos.get("/api/periodos")
    assert response.status_code == 200
    data = response.json()
    assert "anos" in data
    assert "meses" in data
    assert "meses_por_ano" in data
    assert isinstance(data["anos"], list)


def test_listar_periodos_anos_descendente(client_gastos):
    response = client_gastos.get("/api/periodos")
    anos = response.json()["anos"]
    assert anos == sorted(anos, reverse=True)


def test_listar_periodos_sem_dados(client_sem_dados):
    response = client_sem_dados.get("/api/periodos")
    assert response.status_code == 200
    data = response.json()
    assert data["anos"] == []
    assert data["meses"] == []


# ── /api/evolucao/series ──────────────────────────────────────────────────────

def test_listar_series_200(client_gastos):
    response = client_gastos.get("/api/evolucao/series")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_listar_series_estrutura(client_gastos):
    response = client_gastos.get("/api/evolucao/series")
    item = response.json()[0]
    assert "municipio" in item
    assert "serie" in item
    assert isinstance(item["serie"], list)
    ponto = item["serie"][0]
    assert "mes" in ponto
    assert "cesta" in ponto
    assert "componentes" in ponto


def test_listar_series_filtro_municipio(client_gastos):
    # Filtro usa nome sem acento (padrão _normalizar_id esperado pelo use case)
    response = client_gastos.get("/api/evolucao/series?municipios=SAO PAULO")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "São Paulo" in data[0]["municipio"]


def test_listar_series_sem_dados_retorna_lista_vazia(client_sem_dados):
    response = client_sem_dados.get("/api/evolucao/series")
    assert response.status_code == 200
    assert response.json() == []


# ── /api/evolucao/indicadores ─────────────────────────────────────────────────

def test_indicadores_200(client_gastos):
    response = client_gastos.get("/api/evolucao/indicadores")
    assert response.status_code == 200
    data = response.json()
    assert "menor_preco" in data
    assert "variacao_mensal" in data
    assert "variacao_anual" in data
    assert "tendencia" in data


def test_indicadores_sem_dados_retorna_nulos(client_sem_dados):
    response = client_sem_dados.get("/api/evolucao/indicadores")
    assert response.status_code == 200
    data = response.json()
    assert data["menor_preco"] is None
    assert data["variacao_mensal"] is None
    assert data["tendencia"] is None


# ── /api/evolucao/peso-componentes ────────────────────────────────────────────

def test_peso_componentes_200(client_gastos):
    response = client_gastos.get("/api/evolucao/peso-componentes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_peso_componentes_estrutura(client_gastos):
    response = client_gastos.get("/api/evolucao/peso-componentes")
    item = response.json()[0]
    assert "id" in item
    assert "nome" in item
    assert "uf" in item
    assert "rotulo" in item
    assert "total_medio" in item
    assert "componentes" in item
    assert "destaques" in item


def test_peso_componentes_sem_dados(client_sem_dados):
    response = client_sem_dados.get("/api/evolucao/peso-componentes")
    assert response.status_code == 200
    assert response.json() == []


def test_peso_componentes_filtro_municipio(client_gastos):
    response = client_gastos.get("/api/evolucao/peso-componentes?municipios=Curitiba")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "CURITIBA"
