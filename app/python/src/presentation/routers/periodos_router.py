from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.gasto_mensal_repository_impl import SqlGastoMensalRepository
from ...application.use_cases.listar_periodos import ListarPeriodosUseCase

router = APIRouter(prefix="/periodos", tags=["Períodos"])


class PeriodosResponse(BaseModel):
    anos: list[int]
    meses: list[str]
    meses_por_ano: dict[str, list[str]]


@router.get("", response_model=PeriodosResponse)
def listar_periodos(db: Session = Depends(get_db)):
    repo = SqlGastoMensalRepository(db)
    dto = ListarPeriodosUseCase(repo).executar()
    return PeriodosResponse(
        anos=dto.anos,
        meses=dto.meses,
        meses_por_ano={str(k): v for k, v in dto.meses_por_ano.items()},
    )
