from __future__ import annotations
from dataclasses import dataclass, field
from ...domain.value_objects.year_month import YearMonth


@dataclass
class EvolucaoFiltro:
    municipios: list[str] = field(default_factory=list)
    mes_inicio: YearMonth | None = None
    mes_fim: YearMonth | None = None
    ano_referencia: int | None = None

    @property
    def possui_municipios(self) -> bool:
        return bool(self.municipios)

    def municipios_normalizados(self) -> list[str]:
        return [m.strip().upper() for m in self.municipios if m.strip()]
