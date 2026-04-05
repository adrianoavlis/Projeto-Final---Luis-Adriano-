from __future__ import annotations
import pytest
from src.domain.value_objects.municipios import Municipios


def test_todos_municipios_tem_valor():
    assert len(list(Municipios)) == 28


def test_valor_municipio_com_acento():
    assert Municipios.SAO_PAULO.value == "São Paulo"
    assert Municipios.BRASILIA.value == "Brasília"
    assert Municipios.FLORIANOPOLIS.value == "Florianópolis"


def test_normalizado_remove_acentos():
    assert Municipios.SAO_PAULO.normalizado == "SAO PAULO"
    assert Municipios.BRASILIA.normalizado == "BRASILIA"
    assert Municipios.BELEM.normalizado == "BELEM"
    assert Municipios.GOIANIA.normalizado == "GOIANIA"


def test_from_texto_match_exato():
    assert Municipios.from_texto("São Paulo") is Municipios.SAO_PAULO
    assert Municipios.from_texto("Brasília") is Municipios.BRASILIA


def test_from_texto_case_insensitive():
    assert Municipios.from_texto("são paulo") is Municipios.SAO_PAULO
    assert Municipios.from_texto("SÃO PAULO") is Municipios.SAO_PAULO
    assert Municipios.from_texto("BRASILIA") is Municipios.BRASILIA


def test_from_texto_sem_acento():
    assert Municipios.from_texto("Sao Paulo") is Municipios.SAO_PAULO
    assert Municipios.from_texto("Fortaleza") is Municipios.FORTALEZA
    assert Municipios.from_texto("Florianopolis") is Municipios.FLORIANOPOLIS


def test_from_texto_com_espacos():
    assert Municipios.from_texto("  Rio de Janeiro  ") is Municipios.RIO_DE_JANEIRO


def test_from_texto_nao_encontrado_retorna_none():
    assert Municipios.from_texto("Cidade Inexistente") is None
    assert Municipios.from_texto("") is None


def test_municipio_eh_string():
    assert isinstance(Municipios.SAO_PAULO, str)
    assert Municipios.CURITIBA == "Curitiba"


@pytest.mark.parametrize("membro", list(Municipios))
def test_normalizado_nao_tem_acento(membro):
    import unicodedata
    normalizado = membro.normalizado
    for char in normalizado:
        assert unicodedata.category(char) != "Mn", f"{membro.name} tem acento após normalizar: {normalizado}"


@pytest.mark.parametrize("membro", list(Municipios))
def test_from_texto_via_value(membro):
    assert Municipios.from_texto(membro.value) is membro
