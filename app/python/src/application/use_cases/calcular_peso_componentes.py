from __future__ import annotations
from collections import defaultdict
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ...domain.entities.gasto_mensal import COMPONENTES
from ..dtos.evolucao_filtro import EvolucaoFiltro
from ..dtos.peso_componentes_dto import PesoMunicipioDTO, ComponentePesoDTO, PesoDestaquesDTO
from .listar_serie_municipio import ListarSerieMunicipioUseCase, _normalizar_id, _extrair_uf, _fmt_mes


class CalcularPesoComponentesUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo

    def executar(self, filtro: EvolucaoFiltro) -> list[PesoMunicipioDTO]:
        gastos = self._repo.listar_por_filtro(
            mes_inicio=filtro.mes_inicio,
            mes_fim=filtro.mes_fim,
            ano_referencia=filtro.ano_referencia,
        )
        municipios_filtro = {m.upper() for m in filtro.municipios_normalizados()}

        # Agrupa por municipio_id -> componente -> lista de (mes, valor)
        acc: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
        nomes: dict[str, tuple[str, str]] = {}

        for g in gastos:
            nome, uf = _extrair_uf(g.municipio)
            mid = _normalizar_id(nome)
            if municipios_filtro and mid not in municipios_filtro:
                continue
            nomes[mid] = (nome, uf)
            for comp in COMPONENTES:
                v = g.get_componente(comp)
                if v is not None:
                    acc[mid][comp].append((g.mes_ano, float(v)))

        resultado: list[PesoMunicipioDTO] = []
        for mid, comp_data in acc.items():
            nome, uf = nomes.get(mid, (mid, ""))
            componentes: list[ComponentePesoDTO] = []
            soma_medias = 0.0

            for comp in COMPONENTES:
                valores = sorted(comp_data.get(comp, []), key=lambda x: x[0])
                if not valores:
                    continue
                media = sum(v for _, v in valores) / len(valores)
                soma_medias += media
                variacao = None
                if len(valores) >= 2:
                    vi, vf = valores[0][1], valores[-1][1]
                    variacao = ((vf - vi) / vi * 100) if vi > 0 else None
                componentes.append(ComponentePesoDTO(
                    chave=comp,
                    media=round(media, 2),
                    percentual=0.0,
                    variacao=round(variacao, 1) if variacao is not None else None,
                    valor_inicial=round(valores[0][1], 2),
                    valor_final=round(valores[-1][1], 2),
                    mes_inicial=_fmt_mes(valores[0][0].year, valores[0][0].month),
                    mes_final=_fmt_mes(valores[-1][0].year, valores[-1][0].month),
                ))

            if soma_medias > 0:
                for c in componentes:
                    c.percentual = round((c.media / soma_medias) * 100, 1)

            destaques = PesoDestaquesDTO(
                item_mais_caro=max(componentes, key=lambda c: c.media, default=None),
                item_mais_barato=min(componentes, key=lambda c: c.media, default=None),
                maior_aumento=max((c for c in componentes if c.variacao is not None), key=lambda c: c.variacao, default=None),
                maior_reducao=min((c for c in componentes if c.variacao is not None), key=lambda c: c.variacao, default=None),
            )

            meses = sorted({ym for comp_list in comp_data.values() for ym, _ in comp_list})
            resultado.append(PesoMunicipioDTO(
                id=mid,
                nome=nome,
                uf=uf,
                rotulo=f"{nome} / {uf}" if uf else nome,
                periodo_inicio=_fmt_mes(meses[0].year, meses[0].month) if meses else None,
                periodo_fim=_fmt_mes(meses[-1].year, meses[-1].month) if meses else None,
                total_medio=round(soma_medias, 2),
                componentes=componentes,
                destaques=destaques,
            ))
        return resultado
