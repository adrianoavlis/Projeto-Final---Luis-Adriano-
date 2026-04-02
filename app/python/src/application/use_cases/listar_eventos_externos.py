from __future__ import annotations
from datetime import date
from ...domain.repositories.evento_externo_repository import EventoExternoRepository
from ...domain.entities.evento_externo import EventoExterno
from ..dtos.evento_externo_dto import EventoExternoDTO


def _formatar_periodo(d: date) -> str:
    return d.strftime("%m/%Y")


def _to_dto(evento: EventoExterno) -> EventoExternoDTO:
    return EventoExternoDTO(
        id=evento.id,
        titulo=evento.titulo,
        descricao=evento.descricao,
        data_inicio=evento.data_inicio,
        data_fim=evento.data_fim,
        impacto=evento.impacto,
        periodo_inicio=_formatar_periodo(evento.data_inicio),
        periodo_fim=_formatar_periodo(evento.data_fim),
    )


class ListarEventosExternosUseCase:
    def __init__(self, repo: EventoExternoRepository) -> None:
        self._repo = repo

    def executar(
        self, inicio: date | None = None, fim: date | None = None
    ) -> list[EventoExternoDTO]:
        eventos = self._repo.buscar_por_periodo(inicio, fim)
        return [_to_dto(e) for e in sorted(eventos, key=lambda e: (e.data_inicio, e.titulo))]
