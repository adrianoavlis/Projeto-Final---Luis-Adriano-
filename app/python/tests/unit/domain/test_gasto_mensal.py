from decimal import Decimal
from src.domain.entities.gasto_mensal import GastoMensal, COMPONENTES
from src.domain.value_objects.year_month import YearMonth


def _gasto():
    return GastoMensal(
        municipio="São Paulo / SP",
        mes_ano=YearMonth(2023, 1),
        total_cesta=Decimal("700.00"),
        carne=Decimal("200.00"),
        leite=Decimal("100.00"),
    )


def test_get_componente_existente():
    g = _gasto()
    assert g.get_componente("carne") == Decimal("200.00")


def test_get_componente_none():
    g = _gasto()
    assert g.get_componente("arroz") is None


def test_set_componente():
    g = _gasto()
    g.set_componente("arroz", Decimal("50.00"))
    assert g.get_componente("arroz") == Decimal("50.00")


def test_set_componente_invalido_ignorado():
    g = _gasto()
    g.set_componente("xyz", Decimal("10.00"))
    assert not hasattr(g, "xyz") or getattr(g, "xyz", None) != Decimal("10.00")


def test_todos_componentes_definidos():
    assert len(COMPONENTES) == 13
