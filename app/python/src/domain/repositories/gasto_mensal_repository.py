from __future__ import annotations
from abc import ABC, abstractmethod
from ..entities.gasto_mensal import GastoMensal
from ..value_objects.year_month import YearMonth


class GastoMensalRepository(ABC):

    @abstractmethod
    def salvar(self, gasto: GastoMensal) -> GastoMensal:
        ...

    @abstractmethod
    def buscar_por_municipio_e_mes(
        self, municipio: str, mes_ano: YearMonth
    ) -> GastoMensal | None:
        ...

    @abstractmethod
    def listar_todos(self) -> list[GastoMensal]:
        ...

    @abstractmethod
    def listar_por_filtro(
        self,
        mes_inicio: YearMonth | None = None,
        mes_fim: YearMonth | None = None,
        ano_referencia: int | None = None,
    ) -> list[GastoMensal]:
        ...

    @abstractmethod
    def listar_periodos_importados(self) -> list[YearMonth]:
        ...

    @abstractmethod
    def buscar_menor_preco(
        self,
        municipios: list[str],
        mes_inicio: YearMonth | None,
        mes_fim: YearMonth | None,
        ano_referencia: int | None,
    ) -> GastoMensal | None:
        ...
