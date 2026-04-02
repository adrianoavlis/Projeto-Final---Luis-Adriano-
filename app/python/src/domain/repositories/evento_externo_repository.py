from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from ..entities.evento_externo import EventoExterno


class EventoExternoRepository(ABC):

    @abstractmethod
    def salvar(self, evento: EventoExterno) -> EventoExterno:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> EventoExterno | None:
        ...

    @abstractmethod
    def listar_todos(self) -> list[EventoExterno]:
        ...

    @abstractmethod
    def buscar_por_periodo(
        self, inicio: date | None, fim: date | None
    ) -> list[EventoExterno]:
        ...

    @abstractmethod
    def excluir(self, id: int) -> None:
        ...
