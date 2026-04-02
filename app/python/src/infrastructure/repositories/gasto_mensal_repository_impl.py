from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, extract, func

from ...domain.entities.gasto_mensal import GastoMensal, COMPONENTES
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository
from ...domain.value_objects.year_month import YearMonth
from ..database.models import GastoMensalModel


def _ym_to_date(ym: YearMonth) -> date:
    return date(ym.year, ym.month, 1)


def _date_to_ym(d: date) -> YearMonth:
    return YearMonth(d.year, d.month)


def _model_to_entity(m: GastoMensalModel) -> GastoMensal:
    return GastoMensal(
        id=m.id,
        criado_em=m.criado_em,
        atualizado_em=m.atualizado_em,
        municipio=m.municipio,
        mes_ano=_date_to_ym(m.mes_ano),
        total_cesta=m.total_cesta,
        carne=m.carne,
        leite=m.leite,
        feijao=m.feijao,
        arroz=m.arroz,
        farinha=m.farinha,
        batata=m.batata,
        tomate=m.tomate,
        pao=m.pao,
        cafe=m.cafe,
        banana=m.banana,
        acucar=m.acucar,
        oleo=m.oleo,
        manteiga=m.manteiga,
    )


def _entity_to_model(e: GastoMensal, existing: GastoMensalModel | None = None) -> GastoMensalModel:
    m = existing or GastoMensalModel()
    m.municipio = e.municipio
    m.mes_ano = _ym_to_date(e.mes_ano) if e.mes_ano else None
    m.total_cesta = e.total_cesta
    for comp in COMPONENTES:
        setattr(m, comp, e.get_componente(comp))
    return m


class SqlGastoMensalRepository(GastoMensalRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def salvar(self, gasto: GastoMensal) -> GastoMensal:
        if gasto.id is not None:
            model = self._db.get(GastoMensalModel, gasto.id)
            if model is None:
                model = GastoMensalModel()
        else:
            model = GastoMensalModel()
        _entity_to_model(gasto, model)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _model_to_entity(model)

    def buscar_por_municipio_e_mes(self, municipio: str, mes_ano: YearMonth) -> GastoMensal | None:
        stmt = select(GastoMensalModel).where(
            and_(
                GastoMensalModel.municipio == municipio,
                GastoMensalModel.mes_ano == _ym_to_date(mes_ano),
            )
        )
        model = self._db.execute(stmt).scalar_one_or_none()
        return _model_to_entity(model) if model else None

    def listar_todos(self) -> list[GastoMensal]:
        stmt = select(GastoMensalModel).order_by(GastoMensalModel.municipio, GastoMensalModel.mes_ano)
        return [_model_to_entity(m) for m in self._db.execute(stmt).scalars()]

    def listar_por_filtro(
        self,
        mes_inicio: YearMonth | None = None,
        mes_fim: YearMonth | None = None,
        ano_referencia: int | None = None,
    ) -> list[GastoMensal]:
        stmt = select(GastoMensalModel)
        conditions = []
        if mes_inicio:
            conditions.append(GastoMensalModel.mes_ano >= _ym_to_date(mes_inicio))
        if mes_fim:
            conditions.append(GastoMensalModel.mes_ano <= _ym_to_date(mes_fim))
        if ano_referencia:
            conditions.append(extract("year", GastoMensalModel.mes_ano) == ano_referencia)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(GastoMensalModel.municipio, GastoMensalModel.mes_ano)
        return [_model_to_entity(m) for m in self._db.execute(stmt).scalars()]

    def listar_periodos_importados(self) -> list[YearMonth]:
        stmt = select(GastoMensalModel.mes_ano).distinct().order_by(GastoMensalModel.mes_ano)
        rows = self._db.execute(stmt).scalars().all()
        return [_date_to_ym(r) for r in rows]

    def buscar_menor_preco(
        self,
        municipios: list[str],
        mes_inicio: YearMonth | None,
        mes_fim: YearMonth | None,
        ano_referencia: int | None,
    ) -> GastoMensal | None:
        # Subquery: menor total_cesta médio por município no período
        sub = select(
            GastoMensalModel.municipio,
            func.avg(GastoMensalModel.total_cesta).label("media"),
        )
        conditions = []
        if municipios:
            # compara normalizado via UPPER
            conditions.append(func.upper(GastoMensalModel.municipio).in_([m.upper() for m in municipios]))
        if mes_inicio:
            conditions.append(GastoMensalModel.mes_ano >= _ym_to_date(mes_inicio))
        if mes_fim:
            conditions.append(GastoMensalModel.mes_ano <= _ym_to_date(mes_fim))
        if ano_referencia:
            conditions.append(extract("year", GastoMensalModel.mes_ano) == ano_referencia)
        if conditions:
            sub = sub.where(and_(*conditions))
        sub = sub.group_by(GastoMensalModel.municipio).subquery()

        # municipio com menor média
        min_stmt = select(sub.c.municipio).order_by(sub.c.media).limit(1)
        best_mun = self._db.execute(min_stmt).scalar_one_or_none()
        if best_mun is None:
            return None

        # registro do mês mais recente desse município no período
        stmt = select(GastoMensalModel).where(GastoMensalModel.municipio == best_mun)
        if conditions:
            # reaplicar filtros de período
            period_conds = []
            if mes_inicio:
                period_conds.append(GastoMensalModel.mes_ano >= _ym_to_date(mes_inicio))
            if mes_fim:
                period_conds.append(GastoMensalModel.mes_ano <= _ym_to_date(mes_fim))
            if ano_referencia:
                period_conds.append(extract("year", GastoMensalModel.mes_ano) == ano_referencia)
            if period_conds:
                stmt = stmt.where(and_(*period_conds))
        stmt = stmt.order_by(GastoMensalModel.mes_ano.desc()).limit(1)
        model = self._db.execute(stmt).scalar_one_or_none()
        return _model_to_entity(model) if model else None
