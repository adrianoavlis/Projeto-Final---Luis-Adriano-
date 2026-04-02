from __future__ import annotations
import unicodedata
import re
from collections import defaultdict
from decimal import Decimal
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ...domain.entities.gasto_mensal import COMPONENTES
from ..dtos.evolucao_filtro import EvolucaoFiltro
from ..dtos.serie_dto import SerieDTO, SerieMunicipioDTO


MESES_PT = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]


def _fmt_mes(year: int, month: int) -> str:
    return f"{MESES_PT[month-1]}-{year}"


def _normalizar_id(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").upper()


def _extrair_uf(municipio: str) -> tuple[str, str]:
    m = re.search(r"(.+?)\s*[/(]\s*([A-Za-z]{2})\s*[/)]?\s*$", municipio)
    if m:
        return m.group(1).strip(), m.group(2).upper()
    m = re.search(r"(.+?)\s*[-–]\s*([A-Za-z]{2})\s*$", municipio)
    if m:
        return m.group(1).strip(), m.group(2).upper()
    return municipio.strip(), ""


class ListarSerieMunicipioUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo

    def executar(self, filtro: EvolucaoFiltro) -> list[SerieMunicipioDTO]:
        gastos = self._repo.listar_por_filtro(
            mes_inicio=filtro.mes_inicio,
            mes_fim=filtro.mes_fim,
            ano_referencia=filtro.ano_referencia,
        )
        municipios_filtro = {m.upper() for m in filtro.municipios_normalizados()}

        # Agrupa: municipio_id -> mes_ano -> acumulador
        acc: dict[str, dict[tuple[int,int], dict]] = defaultdict(lambda: defaultdict(lambda: {"total": [], "comp": defaultdict(list)}))
        nomes: dict[str, str] = {}

        for g in gastos:
            nome, uf = _extrair_uf(g.municipio)
            mid = _normalizar_id(nome)
            if municipios_filtro and mid not in municipios_filtro and _normalizar_id(g.municipio) not in municipios_filtro:
                continue
            nomes[mid] = f"{nome} / {uf}" if uf else nome
            key = (g.mes_ano.year, g.mes_ano.month)
            if g.total_cesta is not None:
                acc[mid][key]["total"].append(float(g.total_cesta))
            for comp in COMPONENTES:
                v = g.get_componente(comp)
                if v is not None:
                    acc[mid][key]["comp"][comp].append(float(v))

        resultado: list[SerieMunicipioDTO] = []
        for mid, meses in sorted(acc.items()):
            serie: list[SerieDTO] = []
            for (year, month), dados in sorted(meses.items()):
                totais = dados["total"]
                media_total = sum(totais) / len(totais) if totais else 0.0
                comps = {
                    k: round(sum(vs) / len(vs), 2)
                    for k, vs in dados["comp"].items()
                    if vs
                }
                serie.append(SerieDTO(
                    mes=_fmt_mes(year, month),
                    cesta=round(media_total, 2),
                    componentes=comps,
                ))
            resultado.append(SerieMunicipioDTO(municipio=nomes.get(mid, mid), serie=serie))
        return resultado
