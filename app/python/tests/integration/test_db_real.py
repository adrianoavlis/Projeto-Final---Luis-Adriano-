"""
Testes de integração contra o banco SQL Server real.
Usa transações com rollback para não poluir os dados.
"""
from __future__ import annotations
from datetime import date
from decimal import Decimal
import pytest
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import make_engine
from src.infrastructure.repositories.gasto_mensal_repository_impl import SqlGastoMensalRepository
from src.infrastructure.repositories.evento_externo_repository_impl import SqlEventoExternoRepository
from src.domain.entities.evento_externo import EventoExterno
from src.domain.value_objects.impacto import Impacto
from src.domain.value_objects.year_month import YearMonth
from src.application.dtos.evolucao_filtro import EvolucaoFiltro
from src.application.use_cases.listar_municipios import ListarMunicipiosUseCase
from src.application.use_cases.listar_periodos import ListarPeriodosUseCase
from src.application.use_cases.listar_serie_municipio import ListarSerieMunicipioUseCase
from src.application.use_cases.calcular_indicadores import CalcularIndicadoresUseCase
from src.application.use_cases.calcular_peso_componentes import CalcularPesoComponentesUseCase
from src.application.use_cases.criar_evento_externo import CriarEventoExternoUseCase
from src.application.use_cases.excluir_evento_externo import ExcluirEventoExternoUseCase
from src.application.dtos.evento_externo_dto import EventoExternoFormDTO


# ── Fixture: sessão real com rollback ─────────────────────────────────────────

@pytest.fixture
def db():
    """Abre uma sessão real e faz rollback ao final para não persistir dados de teste."""
    engine = make_engine()
    session = Session(engine)
    session.begin()
    yield session
    session.rollback()
    session.close()
    engine.dispose()


# ── GastoMensalRepository ─────────────────────────────────────────────────────

def test_listar_todos_retorna_dados_reais(db):
    repo = SqlGastoMensalRepository(db)
    gastos = repo.listar_todos()
    assert len(gastos) > 0


def test_listar_todos_tem_municipio_e_mes(db):
    repo = SqlGastoMensalRepository(db)
    gastos = repo.listar_todos()
    for g in gastos:
        assert g.municipio
        assert g.mes_ano is not None
        assert g.total_cesta is not None


def test_listar_periodos_importados(db):
    repo = SqlGastoMensalRepository(db)
    periodos = repo.listar_periodos_importados()
    assert len(periodos) > 0
    for p in periodos:
        assert isinstance(p, YearMonth)
        assert 1 <= p.month <= 12
        assert p.year >= 2000


def test_listar_por_filtro_sem_filtro(db):
    repo = SqlGastoMensalRepository(db)
    todos = repo.listar_todos()
    filtrados = repo.listar_por_filtro()
    assert len(filtrados) == len(todos)


def test_listar_por_filtro_com_mes_inicio(db):
    repo = SqlGastoMensalRepository(db)
    filtrados = repo.listar_por_filtro(mes_inicio=YearMonth(2025, 6))
    assert all(g.mes_ano >= YearMonth(2025, 6) for g in filtrados)


def test_listar_por_filtro_com_mes_fim(db):
    repo = SqlGastoMensalRepository(db)
    filtrados = repo.listar_por_filtro(mes_fim=YearMonth(2025, 3))
    assert all(g.mes_ano <= YearMonth(2025, 3) for g in filtrados)


def test_listar_por_filtro_com_intervalo(db):
    repo = SqlGastoMensalRepository(db)
    inicio = YearMonth(2025, 1)
    fim = YearMonth(2025, 6)
    filtrados = repo.listar_por_filtro(mes_inicio=inicio, mes_fim=fim)
    assert len(filtrados) > 0
    assert all(inicio <= g.mes_ano <= fim for g in filtrados)


def test_buscar_menor_preco(db):
    repo = SqlGastoMensalRepository(db)
    gasto = repo.buscar_menor_preco(municipios=[], mes_inicio=None, mes_fim=None, ano_referencia=None)
    assert gasto is not None
    assert gasto.total_cesta is not None
    assert gasto.municipio


def test_buscar_menor_preco_com_municipios(db):
    repo = SqlGastoMensalRepository(db)
    todos = repo.listar_todos()
    muns = list({g.municipio for g in todos})[:3]
    gasto = repo.buscar_menor_preco(municipios=muns, mes_inicio=None, mes_fim=None, ano_referencia=None)
    assert gasto is not None


# ── EventoExternoRepository ───────────────────────────────────────────────────

def test_listar_eventos_retorna_dados(db):
    repo = SqlEventoExternoRepository(db)
    eventos = repo.listar_todos()
    assert isinstance(eventos, list)


def test_crud_evento(db):
    repo = SqlEventoExternoRepository(db)

    # Criar
    evento = EventoExterno(
        titulo="Teste Integração",
        descricao="Criado pelo teste automático",
        data_inicio=date(2025, 3, 1),
        data_fim=date(2025, 3, 31),
        impacto=Impacto.POSITIVO,
    )
    salvo = repo.salvar(evento)
    assert salvo.id is not None
    assert salvo.titulo == "Teste Integração"

    # Buscar por ID
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.titulo == "Teste Integração"
    assert encontrado.impacto == Impacto.POSITIVO

    # Atualizar
    encontrado.titulo = "Teste Atualizado"
    atualizado = repo.salvar(encontrado)
    assert atualizado.titulo == "Teste Atualizado"

    # Excluir
    repo.excluir(salvo.id)
    assert repo.buscar_por_id(salvo.id) is None


def test_buscar_por_periodo(db):
    repo = SqlEventoExternoRepository(db)
    eventos = repo.buscar_por_periodo(date(2020, 1, 1), date(2030, 12, 31))
    assert isinstance(eventos, list)


# ── Use Cases com banco real ──────────────────────────────────────────────────

def test_listar_municipios_use_case(db):
    repo = SqlGastoMensalRepository(db)
    uc = ListarMunicipiosUseCase(repo)
    municipios = uc.executar()
    assert len(municipios) > 0
    assert isinstance(municipios[0], str)
    # Deve estar ordenado
    assert municipios == sorted(municipios, key=lambda x: x.upper().encode('ascii', 'ignore').decode())


def test_listar_periodos_use_case(db):
    repo = SqlGastoMensalRepository(db)
    uc = ListarPeriodosUseCase(repo)
    dto = uc.executar()
    assert len(dto.anos) > 0
    assert len(dto.meses) > 0
    assert dto.anos == sorted(dto.anos, reverse=True)
    for ano in dto.anos:
        assert ano in dto.meses_por_ano


def test_listar_serie_municipio_use_case(db):
    repo = SqlGastoMensalRepository(db)
    uc = ListarSerieMunicipioUseCase(repo)
    series = uc.executar(EvolucaoFiltro())
    assert len(series) > 0
    for s in series:
        assert s.municipio
        assert len(s.serie) > 0
        for ponto in s.serie:
            assert ponto.mes
            assert ponto.cesta >= 0


def test_calcular_indicadores_use_case(db):
    repo = SqlGastoMensalRepository(db)
    uc = CalcularIndicadoresUseCase(repo)
    dto = uc.executar(EvolucaoFiltro())
    assert dto.menor_preco is not None
    assert dto.menor_preco.municipio
    assert dto.variacao_mensal is not None
    assert dto.tendencia is not None


def test_calcular_peso_componentes_use_case(db):
    repo = SqlGastoMensalRepository(db)
    uc = CalcularPesoComponentesUseCase(repo)
    pesos = uc.executar(EvolucaoFiltro())
    assert len(pesos) > 0
    for p in pesos:
        assert p.total_medio > 0
        assert len(p.componentes) > 0
        soma = sum(c.percentual for c in p.componentes)
        assert abs(soma - 100.0) < 0.5  # percentuais somam ~100%


def test_criar_e_excluir_evento_use_case(db):
    repo = SqlEventoExternoRepository(db)
    uc_criar = CriarEventoExternoUseCase(repo)
    uc_excluir = ExcluirEventoExternoUseCase(repo)

    dto_form = EventoExternoFormDTO(
        titulo="Evento Teste UC",
        descricao="Criado pelo use case",
        data_inicio=date(2025, 6, 1),
        data_fim=date(2025, 6, 30),
        impacto=Impacto.NEGATIVO,
    )
    criado = uc_criar.executar(dto_form)
    assert criado.id is not None
    assert criado.titulo == "Evento Teste UC"

    uc_excluir.executar(criado.id)
    assert repo.buscar_por_id(criado.id) is None


# ── API com banco real ────────────────────────────────────────────────────────

@pytest.fixture
def api_client_real(db):
    """TestClient FastAPI usando a sessão real (com rollback)."""
    from fastapi.testclient import TestClient
    from src.main import app
    from src.infrastructure.database.connection import get_db

    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_api_municipios_real(api_client_real):
    response = api_client_real.get("/api/municipios")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(isinstance(m, str) for m in data)


def test_api_periodos_real(api_client_real):
    response = api_client_real.get("/api/periodos")
    assert response.status_code == 200
    data = response.json()
    assert len(data["anos"]) > 0
    assert 2025 in data["anos"]


def test_api_series_real(api_client_real):
    response = api_client_real.get("/api/evolucao/series")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("municipio" in s and "serie" in s for s in data)


def test_api_indicadores_real(api_client_real):
    response = api_client_real.get("/api/evolucao/indicadores")
    assert response.status_code == 200
    data = response.json()
    assert data["menor_preco"] is not None
    assert data["menor_preco"]["municipio"]


def test_api_peso_componentes_real(api_client_real):
    response = api_client_real.get("/api/evolucao/peso-componentes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["total_medio"] > 0
        assert len(item["componentes"]) > 0


def test_api_eventos_crud_real(api_client_real):
    # Criar
    response = api_client_real.post("/api/eventos", json={
        "titulo": "Evento API Teste",
        "descricao": "Teste via API real",
        "data_inicio": "2025-05-01",
        "data_fim": "2025-05-31",
        "impacto": "POSITIVO",
    })
    assert response.status_code == 201
    evento_id = response.json()["id"]

    # Listar
    response = api_client_real.get("/api/eventos")
    assert response.status_code == 200
    titulos = [e["titulo"] for e in response.json()]
    assert "Evento API Teste" in titulos

    # Atualizar
    response = api_client_real.put(f"/api/eventos/{evento_id}", json={
        "titulo": "Evento Atualizado",
        "descricao": "Atualizado",
        "data_inicio": "2025-05-01",
        "data_fim": "2025-05-31",
        "impacto": "NEGATIVO",
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Evento Atualizado"

    # Excluir
    response = api_client_real.delete(f"/api/eventos/{evento_id}")
    assert response.status_code == 204
