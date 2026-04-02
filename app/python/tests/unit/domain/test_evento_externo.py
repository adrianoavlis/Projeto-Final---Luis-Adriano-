import pytest
from datetime import date
from src.domain.entities.evento_externo import EventoExterno
from src.domain.value_objects.impacto import Impacto


def _evento_valido(**kwargs):
    defaults = dict(
        titulo="Greve dos Caminhoneiros",
        descricao="Impacto no abastecimento",
        data_inicio=date(2023, 5, 1),
        data_fim=date(2023, 5, 15),
        impacto=Impacto.NEGATIVO,
    )
    defaults.update(kwargs)
    return EventoExterno(**defaults)


def test_evento_valido():
    e = _evento_valido()
    assert e.validar() == []


def test_titulo_obrigatorio():
    e = _evento_valido(titulo="")
    erros = e.validar()
    assert any("Título" in err for err in erros)


def test_titulo_muito_longo():
    e = _evento_valido(titulo="x" * 151)
    erros = e.validar()
    assert any("150" in err for err in erros)


def test_data_inicio_obrigatoria():
    e = _evento_valido(data_inicio=None)
    erros = e.validar()
    assert any("início" in err for err in erros)


def test_data_fim_obrigatoria():
    e = _evento_valido(data_fim=None)
    erros = e.validar()
    assert any("fim" in err for err in erros)


def test_data_fim_antes_de_inicio():
    e = _evento_valido(data_inicio=date(2023, 5, 15), data_fim=date(2023, 5, 1))
    erros = e.validar()
    assert any(">=" in err or "fim" in err.lower() for err in erros)


def test_impacto_obrigatorio():
    e = _evento_valido(impacto=None)
    erros = e.validar()
    assert any("Impacto" in err for err in erros)


def test_titulo_strip():
    e = EventoExterno(
        titulo="  Evento  ",
        descricao="",
        data_inicio=date(2023, 1, 1),
        data_fim=date(2023, 1, 31),
        impacto=Impacto.POSITIVO,
    )
    assert e.titulo == "Evento"
