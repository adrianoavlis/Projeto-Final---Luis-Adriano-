from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from .base import BaseEntity
from ..value_objects.impacto import Impacto


@dataclass
class EventoExterno(BaseEntity):
    titulo: str = ""
    descricao: str = ""
    data_inicio: date | None = None
    data_fim: date | None = None
    impacto: Impacto | None = None

    def __post_init__(self) -> None:
        if self.titulo:
            self.titulo = self.titulo.strip()
        if self.descricao:
            self.descricao = self.descricao.strip()

    def validar(self) -> list[str]:
        erros: list[str] = []
        if not self.titulo:
            erros.append("Título é obrigatório.")
        if len(self.titulo) > 150:
            erros.append("Título deve ter no máximo 150 caracteres.")
        if self.data_inicio is None:
            erros.append("Data de início é obrigatória.")
        if self.data_fim is None:
            erros.append("Data de fim é obrigatória.")
        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            erros.append("Data de fim deve ser >= data de início.")
        if self.impacto is None:
            erros.append("Impacto é obrigatório.")
        return erros
