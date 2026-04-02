import pytest
from src.domain.value_objects.year_month import YearMonth


def test_from_string_iso():
    ym = YearMonth.from_string("2023-01")
    assert ym.year == 2023
    assert ym.month == 1


def test_from_string_br():
    ym = YearMonth.from_string("03/2022")
    assert ym.year == 2022
    assert ym.month == 3


def test_from_string_six_digits():
    ym = YearMonth.from_string("012023")
    assert ym.year == 2023
    assert ym.month == 1


def test_to_iso():
    assert YearMonth(2023, 5).to_iso() == "2023-05"


def test_to_display():
    assert YearMonth(2023, 5).to_display() == "05/2023"


def test_invalid_month():
    with pytest.raises(ValueError):
        YearMonth(2023, 13)


def test_invalid_year():
    with pytest.raises(ValueError):
        YearMonth(1800, 1)


def test_ordering():
    a = YearMonth(2022, 1)
    b = YearMonth(2022, 12)
    c = YearMonth(2023, 1)
    assert a < b < c


def test_invalid_format():
    with pytest.raises(ValueError):
        YearMonth.from_string("not-a-date")
