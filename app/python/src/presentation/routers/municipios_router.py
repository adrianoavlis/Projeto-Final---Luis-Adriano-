from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.gasto_mensal_repository_impl import SqlGastoMensalRepository
from ...application.use_cases.listar_municipios import ListarMunicipiosUseCase

router = APIRouter(prefix="/municipios", tags=["Municípios"])


@router.get("", response_model=list[str])
def listar_municipios(db: Session = Depends(get_db)):
    repo = SqlGastoMensalRepository(db)
    return ListarMunicipiosUseCase(repo).executar()
