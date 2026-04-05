from __future__ import annotations
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ...domain.value_objects.year_month import YearMonth
from ..dtos.dados_dto import GastoMensalItemDTO, PaginaGastosDTO


class ListarDadosUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo

    def executar(
        self,
        municipio: str | None,
        periodo: str | None,
        pagina: int,
        tamanho: int,
    ) -> PaginaGastosDTO:
        total, gastos = self._repo.listar_paginado(
            municipio=municipio,
            periodo=periodo,
            pagina=pagina,
            tamanho=tamanho,
        )
        total_paginas = max(1, (total + tamanho - 1) // tamanho)
        itens = [
            GastoMensalItemDTO(
                id=g.id,
                municipio=g.municipio,
                periodo=g.mes_ano.to_display() if g.mes_ano else "",
                total_cesta=float(g.total_cesta) if g.total_cesta is not None else 0.0,
                carne=float(g.carne) if g.carne is not None else None,
                leite=float(g.leite) if g.leite is not None else None,
                feijao=float(g.feijao) if g.feijao is not None else None,
                arroz=float(g.arroz) if g.arroz is not None else None,
                farinha=float(g.farinha) if g.farinha is not None else None,
                batata=float(g.batata) if g.batata is not None else None,
                tomate=float(g.tomate) if g.tomate is not None else None,
                pao=float(g.pao) if g.pao is not None else None,
                cafe=float(g.cafe) if g.cafe is not None else None,
                banana=float(g.banana) if g.banana is not None else None,
                acucar=float(g.acucar) if g.acucar is not None else None,
                oleo=float(g.oleo) if g.oleo is not None else None,
                manteiga=float(g.manteiga) if g.manteiga is not None else None,
            )
            for g in gastos
        ]
        return PaginaGastosDTO(
            itens=itens,
            total=total,
            pagina=pagina,
            tamanho=tamanho,
            total_paginas=total_paginas,
        )
