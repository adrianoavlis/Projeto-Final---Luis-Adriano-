from __future__ import annotations
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from ...domain.entities.evento_externo import EventoExterno
from ...domain.repositories.evento_externo_repository import EventoExternoRepository
from ...domain.value_objects.impacto import Impacto
from ..database.models import EventoExternoModel


def _model_to_entity(m: EventoExternoModel) -> EventoExterno:
    return EventoExterno(
        id=m.id,
        criado_em=m.criado_em,
        atualizado_em=m.atualizado_em,
        titulo=m.titulo,
        descricao=m.descricao or "",
        data_inicio=m.data_inicio,
        data_fim=m.data_fim,
        impacto=Impacto(m.impacto),
    )


def _entity_to_model(e: EventoExterno, existing: EventoExternoModel | None = None) -> EventoExternoModel:
    now = datetime.now(tz=timezone.utc)
    m = existing or EventoExternoModel()
    m.titulo = e.titulo
    m.descricao = e.descricao or None
    m.data_inicio = e.data_inicio
    m.data_fim = e.data_fim
    m.impacto = e.impacto.value if e.impacto else None
    if m.criado_em is None:
        m.criado_em = now
    m.atualizado_em = now
    return m


class SqlEventoExternoRepository(EventoExternoRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def salvar(self, evento: EventoExterno) -> EventoExterno:
        if evento.id is not None:
            model = self._db.get(EventoExternoModel, evento.id)
            if model is None:
                model = EventoExternoModel()
        else:
            model = EventoExternoModel()
        _entity_to_model(evento, model)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _model_to_entity(model)

    def buscar_por_id(self, id: int) -> EventoExterno | None:
        model = self._db.get(EventoExternoModel, id)
        return _model_to_entity(model) if model else None

    def listar_todos(self) -> list[EventoExterno]:
        stmt = select(EventoExternoModel).order_by(EventoExternoModel.data_inicio)
        return [_model_to_entity(m) for m in self._db.execute(stmt).scalars()]

    def buscar_por_periodo(self, inicio: date | None, fim: date | None) -> list[EventoExterno]:
        stmt = select(EventoExternoModel)
        conditions = []
        if inicio:
            conditions.append(EventoExternoModel.data_fim >= inicio)
        if fim:
            conditions.append(EventoExternoModel.data_inicio <= fim)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(EventoExternoModel.data_inicio)
        return [_model_to_entity(m) for m in self._db.execute(stmt).scalars()]

    def excluir(self, id: int) -> None:
        model = self._db.get(EventoExternoModel, id)
        if model:
            self._db.delete(model)
            self._db.commit()
