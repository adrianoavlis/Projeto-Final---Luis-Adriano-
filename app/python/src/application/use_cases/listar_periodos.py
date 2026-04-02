from __future__ import annotations
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ..dtos.serie_dto import PeriodosDisponiveisDTO


class ListarPeriodosUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo

    def executar(self) -> PeriodosDisponiveisDTO:
        periodos = self._repo.listar_periodos_importados()
        anos = sorted({p.year for p in periodos}, reverse=True)
        meses = sorted({p.to_iso() for p in periodos})
        meses_por_ano: dict[int, list[str]] = {}
        for p in periodos:
            meses_por_ano.setdefault(p.year, [])
            iso = p.to_iso()
            if iso not in meses_por_ano[p.year]:
                meses_por_ano[p.year].append(iso)
        for k in meses_por_ano:
            meses_por_ano[k].sort()
        return PeriodosDisponiveisDTO(anos=anos, meses=meses, meses_por_ano=meses_por_ano)
