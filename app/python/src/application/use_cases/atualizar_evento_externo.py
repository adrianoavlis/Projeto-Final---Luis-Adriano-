from __future__ import annotations
from ...domain.repositories.evento_externo_repository import EventoExternoRepository
from ...domain.exceptions import EntidadeNaoEncontradaException, ValidacaoException
from ..dtos.evento_externo_dto import EventoExternoFormDTO, EventoExternoDTO
from .listar_eventos_externos import _to_dto


class AtualizarEventoExternoUseCase:
    def __init__(self, repo: EventoExternoRepository) -> None:
        self._repo = repo

    def executar(self, id: int, form: EventoExternoFormDTO) -> EventoExternoDTO:
        evento = self._repo.buscar_por_id(id)
        if evento is None:
            raise EntidadeNaoEncontradaException("EventoExterno", id)
        evento.titulo = form.titulo.strip()
        evento.descricao = (form.descricao or "").strip()
        evento.data_inicio = form.data_inicio
        evento.data_fim = form.data_fim
        evento.impacto = form.impacto
        erros = evento.validar()
        if erros:
            raise ValidacaoException(erros)
        salvo = self._repo.salvar(evento)
        return _to_dto(salvo)
