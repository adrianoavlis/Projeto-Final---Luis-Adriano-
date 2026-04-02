from __future__ import annotations
from datetime import date
from unittest.mock import MagicMock
import pytest

from src.domain.entities.evento_externo import EventoExterno
from src.domain.value_objects.impacto import Impacto
from src.domain.exceptions import ValidacaoException, EntidadeNaoEncontradaException
from src.application.dtos.evento_externo_dto import EventoExternoFormDTO
from src.application.use_cases.criar_evento_externo import CriarEventoExternoUseCase
from src.application.use_cases.atualizar_evento_externo import AtualizarEventoExternoUseCase
from src.application.use_cases.excluir_evento_externo import ExcluirEventoExternoUseCase
from src.application.use_cases.listar_eventos_externos import ListarEventosExternosUseCase


def _form(**kwargs):
    defaults = dict(
        titulo="Greve",
        descricao="Desc",
        data_inicio=date(2023, 5, 1),
        data_fim=date(2023, 5, 15),
        impacto=Impacto.NEGATIVO,
    )
    defaults.update(kwargs)
    return EventoExternoFormDTO(**defaults)


def _evento_salvo():
    return EventoExterno(
        id=1,
        titulo="Greve",
        descricao="Desc",
        data_inicio=date(2023, 5, 1),
        data_fim=date(2023, 5, 15),
        impacto=Impacto.NEGATIVO,
    )


def test_criar_evento_valido():
    repo = MagicMock()
    repo.salvar.return_value = _evento_salvo()
    dto = CriarEventoExternoUseCase(repo).executar(_form())
    assert dto.id == 1
    assert dto.titulo == "Greve"
    repo.salvar.assert_called_once()


def test_criar_evento_titulo_vazio_levanta_excecao():
    repo = MagicMock()
    with pytest.raises(ValidacaoException):
        CriarEventoExternoUseCase(repo).executar(_form(titulo=""))


def test_atualizar_evento_nao_encontrado():
    repo = MagicMock()
    repo.buscar_por_id.return_value = None
    with pytest.raises(EntidadeNaoEncontradaException):
        AtualizarEventoExternoUseCase(repo).executar(99, _form())


def test_atualizar_evento_valido():
    repo = MagicMock()
    repo.buscar_por_id.return_value = _evento_salvo()
    repo.salvar.return_value = EventoExterno(
        id=1,
        titulo="Greve Atualizada",
        descricao="Nova desc",
        data_inicio=date(2023, 5, 1),
        data_fim=date(2023, 5, 20),
        impacto=Impacto.NEGATIVO,
    )
    dto = AtualizarEventoExternoUseCase(repo).executar(1, _form(titulo="Greve Atualizada", data_fim=date(2023, 5, 20)))
    assert dto.titulo == "Greve Atualizada"


def test_excluir_evento_chama_repo():
    repo = MagicMock()
    ExcluirEventoExternoUseCase(repo).executar(1)
    repo.excluir.assert_called_once_with(1)


def test_listar_eventos_ordenados():
    repo = MagicMock()
    repo.buscar_por_periodo.return_value = [
        EventoExterno(id=2, titulo="B", descricao="", data_inicio=date(2023, 3, 1), data_fim=date(2023, 3, 5), impacto=Impacto.POSITIVO),
        EventoExterno(id=1, titulo="A", descricao="", data_inicio=date(2023, 1, 1), data_fim=date(2023, 1, 31), impacto=Impacto.NEGATIVO),
    ]
    dtos = ListarEventosExternosUseCase(repo).executar()
    assert dtos[0].titulo == "A"
    assert dtos[1].titulo == "B"
