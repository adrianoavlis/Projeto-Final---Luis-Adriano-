from __future__ import annotations
from ...domain.repositories.evento_externo_repository import EventoExternoRepository


class ExcluirEventoExternoUseCase:
    def __init__(self, repo: EventoExternoRepository) -> None:
        self._repo = repo

    def executar(self, id: int) -> None:
        self._repo.excluir(id)
