from __future__ import annotations
import unicodedata
import re
from collections import defaultdict
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ..dtos.evolucao_filtro import EvolucaoFiltro
from ..dtos.indicadores_dto import IndicadoresDTO, IndicadorPrecoDTO, VariacaoDTO, TendenciaDTO
from ..dtos.serie_dto import SerieDTO
from .listar_serie_municipio import ListarSerieMunicipioUseCase, _normalizar_id, _extrair_uf, MESES_PT


def _fmt_mes(year: int, month: int) -> str:
    return f"{MESES_PT[month-1]}-{year}"


class CalcularIndicadoresUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo
        self._serie_uc = ListarSerieMunicipioUseCase(repo)

    def executar(self, filtro: EvolucaoFiltro) -> IndicadoresDTO:
        series = self._serie_uc.executar(filtro)
        if not series:
            return IndicadoresDTO(None, None, None, None)
        return IndicadoresDTO(
            menor_preco=self._calcular_menor_preco(filtro),
            variacao_mensal=self._calcular_variacao_mensal(series),
            variacao_anual=self._calcular_variacao_anual(series, filtro.ano_referencia),
            tendencia=self._calcular_tendencia(series),
        )

    def _calcular_menor_preco(self, filtro: EvolucaoFiltro) -> IndicadorPrecoDTO | None:
        municipios = filtro.municipios_normalizados()
        gasto = self._repo.buscar_menor_preco(
            municipios=municipios,
            mes_inicio=filtro.mes_inicio,
            mes_fim=filtro.mes_fim,
            ano_referencia=filtro.ano_referencia,
        )
        if gasto is None or gasto.total_cesta is None:
            return None
        nome, uf = _extrair_uf(gasto.municipio)
        mid = _normalizar_id(nome)
        mes = gasto.mes_ano.to_iso() if gasto.mes_ano else ""
        mes_desc = _fmt_mes(gasto.mes_ano.year, gasto.mes_ano.month) if gasto.mes_ano else ""
        return IndicadorPrecoDTO(
            valor=float(gasto.total_cesta),
            municipio=f"{nome} / {uf}" if uf else nome,
            municipio_id=mid,
            mes=mes,
            mes_descricao=mes_desc,
            observacao=f"{nome} • {mes_desc}",
        )

    def _calcular_variacao_mensal(self, series: list) -> VariacaoDTO | None:
        variacoes: list[float] = []
        for s in series:
            vals = [p.cesta for p in s.serie if p.cesta > 0]
            if len(vals) >= 2:
                var = ((vals[-1] - vals[-2]) / vals[-2]) * 100
                variacoes.append(var)
        if not variacoes:
            return None
        media = sum(variacoes) / len(variacoes)
        sinal = "+" if media >= 0 else ""
        return VariacaoDTO(
            percentual=round(media, 1),
            descricao=f"Variação mensal média: {sinal}{media:.1f}%",
            municipios_considerados=len(variacoes),
        )

    def _calcular_variacao_anual(self, series: list, ano_referencia: int | None) -> VariacaoDTO | None:
        variacoes: list[float] = []
        for s in series:
            vals = s.serie
            if ano_referencia:
                vals = [p for p in vals if str(ano_referencia) in p.mes]
            nums = [p.cesta for p in vals if p.cesta > 0]
            if len(nums) >= 2:
                var = ((nums[-1] - nums[0]) / nums[0]) * 100
                variacoes.append(var)
        if not variacoes:
            return None
        media = sum(variacoes) / len(variacoes)
        sinal = "+" if media >= 0 else ""
        return VariacaoDTO(
            percentual=round(media, 1),
            descricao=f"Variação anual média: {sinal}{media:.1f}%",
            municipios_considerados=len(variacoes),
        )

    def _calcular_tendencia(self, series: list) -> TendenciaDTO | None:
        slopes: list[float] = []
        for s in series:
            vals = [p.cesta for p in s.serie if p.cesta > 0]
            if len(vals) < 2:
                continue
            n = len(vals)
            sx = sum(range(n))
            sy = sum(vals)
            sxy = sum(i * v for i, v in enumerate(vals))
            sxx = sum(i * i for i in range(n))
            denom = n * sxx - sx * sx
            if denom == 0:
                continue
            slope = (n * sxy - sx * sy) / denom
            media = sy / n
            if media > 0:
                slopes.append((slope / media) * 100)
        if not slopes:
            return None
        media_slope = sum(slopes) / len(slopes)
        if media_slope > 0.6:
            status, texto = "ALTA", "Tendência de alta acentuada"
        elif media_slope > 0.2:
            status, texto = "ALTA", "Tendência de alta moderada"
        elif media_slope < -0.6:
            status, texto = "QUEDA", "Tendência de queda acentuada"
        elif media_slope < -0.2:
            status, texto = "QUEDA", "Tendência de queda moderada"
        else:
            status, texto = "ESTAVEL", "Tendência estável"
        sinal = "+" if media_slope >= 0 else ""
        return TendenciaDTO(
            percentual=round(media_slope, 2),
            texto=texto,
            descricao=f"Inclinação média: {sinal}{media_slope:.2f}% por período",
            status=status,
            municipios_considerados=len(slopes),
        )
