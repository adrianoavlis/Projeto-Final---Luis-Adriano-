from __future__ import annotations
import unicodedata
from enum import Enum


def _normalizar(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return sem_acento.upper()


class Municipios(str, Enum):
    ARACAJU = "Aracaju"
    BELEM = "Belém"
    BELO_HORIZONTE = "Belo Horizonte"
    BOA_VISTA = "Boa Vista"
    BRASILIA = "Brasília"
    CAMPO_GRANDE = "Campo Grande"
    CUIABA = "Cuiabá"
    CURITIBA = "Curitiba"
    FLORIANOPOLIS = "Florianópolis"
    FORTALEZA = "Fortaleza"
    GOIANIA = "Goiânia"
    JOAO_PESSOA = "João Pessoa"
    MACAE = "Macaé"
    MACAPA = "Macapá"
    MACEIO = "Maceió"
    MANAUS = "Manaus"
    NATAL = "Natal"
    PALMAS = "Palmas"
    PORTO_ALEGRE = "Porto Alegre"
    PORTO_VELHO = "Porto Velho"
    RECIFE = "Recife"
    RIO_BRANCO = "Rio Branco"
    RIO_DE_JANEIRO = "Rio de Janeiro"
    SALVADOR = "Salvador"
    SAO_LUIS = "São Luís"
    SAO_PAULO = "São Paulo"
    TERESINA = "Teresina"
    VITORIA = "Vitória"

    @property
    def normalizado(self) -> str:
        return _normalizar(self.value)

    @classmethod
    def from_texto(cls, texto: str) -> "Municipios | None":
        normalizado = _normalizar(texto.strip())
        for m in cls:
            if m.normalizado == normalizado:
                return m
        return None
