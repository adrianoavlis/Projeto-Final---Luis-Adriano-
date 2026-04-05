from __future__ import annotations
import unicodedata
from ...domain.repositories.gasto_mensal_repository import GastoMensalRepository


def _normalizar_id(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").upper()


def _extrair_uf(municipio: str) -> tuple[str, str]:
    """Retorna (nome_sem_uf, uf)."""
    import re
    m = re.search(r"(.+?)\s*[/(]\s*([A-Za-z]{2})\s*[/)]?\s*$", municipio)
    if m:
        return m.group(1).strip(), m.group(2).upper()
    m = re.search(r"(.+?)\s*[-–]\s*([A-Za-z]{2})\s*$", municipio)
    if m:
        return m.group(1).strip(), m.group(2).upper()
    return municipio.strip(), ""


class ListarMunicipiosUseCase:
    def __init__(self, repo: GastoMensalRepository) -> None:
        self._repo = repo

    def executar(self) -> list[str]:
        gastos = self._repo.listar_todos()
        vistos: dict[str, str] = {}
        for g in gastos:
            if not g.municipio:
                continue
            nome, uf = _extrair_uf(g.municipio)
            mid = _normalizar_id(nome)
            label = f"{nome} / {uf}" if uf else nome
            vistos[mid] = label
        return sorted(vistos.values(), key=lambda x: _normalizar_id(x))
