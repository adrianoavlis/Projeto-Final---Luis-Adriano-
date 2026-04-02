from __future__ import annotations
from ...domain.repositories.evento_externo_repository import EventoExternoRepository
from ...domain.entities.evento_externo import EventoExterno
from ...domain.exceptions import ValidacaoException
from ..dtos.evento_externo_dto import EventoExternoFormDTO, EventoExternoDTO
from .listar_eventos_externos import _to_dto


class CriarEventoExternoUseCase:
    def __init__(self, repo: EventoExternoRepository) -> None:
        self._repo = repo

    def executar(self, form: EventoExternoFormDTO) -> EventoExternoDTO:
        evento = EventoExterno(
            titulo=form.titulo,
            descricao=form.descricao or "",
            data_inicio=form.data_inicio,
            data_fim=form.data_fim,
            impacto=form.impacto,
        )
        erros = evento.validar()
        if erros:
            raise ValidacaoException(erros)
        salvo = self._repo.salvar(evento)
        return _to_dto(salvo)
