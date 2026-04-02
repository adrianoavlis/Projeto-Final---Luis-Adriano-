from __future__ import annotations
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.evento_externo_repository_impl import SqlEventoExternoRepository
from ...application.use_cases.listar_eventos_externos import ListarEventosExternosUseCase
from ...application.use_cases.criar_evento_externo import CriarEventoExternoUseCase
from ...application.use_cases.atualizar_evento_externo import AtualizarEventoExternoUseCase
from ...application.use_cases.excluir_evento_externo import ExcluirEventoExternoUseCase
from ...application.dtos.evento_externo_dto import EventoExternoFormDTO
from ...domain.value_objects.impacto import Impacto
from ...domain.exceptions import EntidadeNaoEncontradaException, ValidacaoException

router = APIRouter(prefix="/eventos", tags=["Eventos Externos"])


class EventoRequest(BaseModel):
    titulo: str
    descricao: str = ""
    data_inicio: date
    data_fim: date
    impacto: Impacto

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Título não pode ser vazio.")
        return v.strip()


class EventoResponse(BaseModel):
    id: Optional[int]
    titulo: str
    descricao: str
    data_inicio: date
    data_fim: date
    impacto: Impacto
    periodo_inicio: str
    periodo_fim: str


@router.get("", response_model=list[EventoResponse])
def listar_eventos(
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    db: Session = Depends(get_db),
):
    repo = SqlEventoExternoRepository(db)
    eventos = ListarEventosExternosUseCase(repo).executar(inicio, fim)
    return [EventoResponse(**vars(e)) for e in eventos]


@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(body: EventoRequest, db: Session = Depends(get_db)):
    repo = SqlEventoExternoRepository(db)
    form = EventoExternoFormDTO(
        titulo=body.titulo,
        descricao=body.descricao,
        data_inicio=body.data_inicio,
        data_fim=body.data_fim,
        impacto=body.impacto,
    )
    try:
        dto = CriarEventoExternoUseCase(repo).executar(form)
    except ValidacaoException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.erros)
    return EventoResponse(**vars(dto))


@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int, body: EventoRequest, db: Session = Depends(get_db)):
    repo = SqlEventoExternoRepository(db)
    form = EventoExternoFormDTO(
        id=evento_id,
        titulo=body.titulo,
        descricao=body.descricao,
        data_inicio=body.data_inicio,
        data_fim=body.data_fim,
        impacto=body.impacto,
    )
    try:
        dto = AtualizarEventoExternoUseCase(repo).executar(evento_id, form)
    except EntidadeNaoEncontradaException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValidacaoException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.erros)
    return EventoResponse(**vars(dto))


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(evento_id: int, db: Session = Depends(get_db)):
    repo = SqlEventoExternoRepository(db)
    ExcluirEventoExternoUseCase(repo).executar(evento_id)
