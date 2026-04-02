from __future__ import annotations
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.infrastructure.database.connection import get_db
from src.domain.entities.evento_externo import EventoExterno
from src.domain.value_objects.impacto import Impacto


# ── Fake DB session ──────────────────────────────────────────────────────────

def _make_fake_db(eventos: list[EventoExterno]):
    from src.infrastructure.repositories.evento_externo_repository_impl import SqlEventoExternoRepository
    fake_session = MagicMock()
    # patch get to return by id
    by_id = {e.id: e for e in eventos}

    from src.infrastructure.database.models import EventoExternoModel
    def _get(model_class, pk):
        if model_class is EventoExternoModel:
            e = by_id.get(pk)
            if e is None:
                return None
            m = EventoExternoModel()
            m.id = e.id
            m.titulo = e.titulo
            m.descricao = e.descricao
            m.data_inicio = e.data_inicio
            m.data_fim = e.data_fim
            m.impacto = e.impacto.value
            m.criado_em = None
            m.atualizado_em = None
            return m
        return None

    fake_session.get.side_effect = _get
    return fake_session


# ── Tests ────────────────────────────────────────────────────────────────────

def _evento(id=1):
    return EventoExterno(
        id=id,
        titulo="Greve dos Caminhoneiros",
        descricao="Impacto no abastecimento",
        data_inicio=date(2018, 5, 21),
        data_fim=date(2018, 5, 30),
        impacto=Impacto.NEGATIVO,
    )


@pytest.fixture
def client_with_evento():
    evento = _evento()
    from src.infrastructure.database.models import EventoExternoModel
    model = EventoExternoModel()
    model.id = evento.id
    model.titulo = evento.titulo
    model.descricao = evento.descricao
    model.data_inicio = evento.data_inicio
    model.data_fim = evento.data_fim
    model.impacto = evento.impacto.value
    model.criado_em = None
    model.atualizado_em = None

    fake_session = MagicMock()
    fake_session.get.return_value = model

    from sqlalchemy import Result
    fake_scalars = MagicMock()
    fake_scalars.__iter__ = MagicMock(return_value=iter([model]))
    fake_result = MagicMock()
    fake_result.scalars.return_value = fake_scalars
    fake_session.execute.return_value = fake_result

    def saved_model():
        m2 = EventoExternoModel()
        m2.id = 1
        m2.titulo = model.titulo
        m2.descricao = model.descricao
        m2.data_inicio = model.data_inicio
        m2.data_fim = model.data_fim
        m2.impacto = model.impacto
        m2.criado_em = None
        m2.atualizado_em = None
        return m2

    fake_session.refresh.side_effect = lambda m: None

    app.dependency_overrides[get_db] = lambda: fake_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_listar_eventos_200(client_with_evento):
    response = client_with_evento.get("/api/eventos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["titulo"] == "Greve dos Caminhoneiros"


def test_criar_evento_201():
    fake_session = MagicMock()
    from src.infrastructure.database.models import EventoExternoModel
    created = EventoExternoModel()
    created.id = 2
    created.titulo = "Novo Evento"
    created.descricao = ""
    created.data_inicio = date(2023, 1, 1)
    created.data_fim = date(2023, 1, 31)
    created.impacto = "POSITIVO"
    created.criado_em = None
    created.atualizado_em = None
    fake_session.refresh.side_effect = lambda m: setattr(m, "id", 2) or setattr(m, "criado_em", None) or setattr(m, "atualizado_em", None)

    app.dependency_overrides[get_db] = lambda: fake_session
    client = TestClient(app)
    try:
        response = client.post("/api/eventos", json={
            "titulo": "Novo Evento",
            "descricao": "",
            "data_inicio": "2023-01-01",
            "data_fim": "2023-01-31",
            "impacto": "POSITIVO",
        })
        assert response.status_code == 201
    finally:
        app.dependency_overrides.clear()


def test_criar_evento_titulo_vazio_422():
    fake_session = MagicMock()
    app.dependency_overrides[get_db] = lambda: fake_session
    client = TestClient(app)
    try:
        response = client.post("/api/eventos", json={
            "titulo": "",
            "data_inicio": "2023-01-01",
            "data_fim": "2023-01-31",
            "impacto": "POSITIVO",
        })
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_excluir_evento_204():
    fake_session = MagicMock()
    from src.infrastructure.database.models import EventoExternoModel
    m = EventoExternoModel()
    m.id = 1
    fake_session.get.return_value = m
    app.dependency_overrides[get_db] = lambda: fake_session
    client = TestClient(app)
    try:
        response = client.delete("/api/eventos/1")
        assert response.status_code == 204
        fake_session.delete.assert_called_once_with(m)
    finally:
        app.dependency_overrides.clear()


def test_health():
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
