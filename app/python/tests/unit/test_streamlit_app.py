"""Testes da camada de dados do app Streamlit (sem iniciar servidor)."""
from __future__ import annotations
from datetime import date
from unittest.mock import patch, MagicMock
import sys, os

# Garante que src e raiz do projeto estão no path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# ── Helpers importados diretamente ──────────────────────────────────────────

def _import_app():
    """Importa o módulo sem executar st.set_page_config (que exige runtime)."""
    import importlib, types

    def _noop(*a, **kw):
        return None

    class _CacheData:
        def __call__(self, *a, **kw):
            def decorator(f):
                # expõe __wrapped__ para os testes chamarem sem cache
                f.__wrapped__ = f
                return f
            return decorator
        def clear(self):
            pass

    st_stub = types.ModuleType("streamlit")
    # atributos usados no módulo em nível de import
    for attr in (
        "set_page_config", "markdown", "header", "subheader", "caption",
        "info", "warning", "error", "success", "divider", "title",
        "spinner", "expander", "container", "columns", "tabs",
        "multiselect", "selectbox", "text_input", "text_area",
        "date_input", "form", "form_submit_button", "radio",
        "metric", "dataframe", "plotly_chart", "rerun",
        "sidebar", "session_state",
    ):
        setattr(st_stub, attr, _noop)
    st_stub.session_state = {}
    st_stub.cache_data = _CacheData()
    sys.modules["streamlit"] = st_stub

    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location(
        "streamlit_app",
        pathlib.Path(__file__).parents[2] / "streamlit_app.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


_app = _import_app()


# ── Testes de get_municipios ──────────────────────────────────────────────────

def test_get_municipios_sucesso():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = ["São Paulo / SP", "Curitiba / PR"]
        mock_get.return_value.ok = True
        result = _app.get_municipios.__wrapped__()  # ignora cache
        assert "São Paulo / SP" in result


def test_get_municipios_falha_retorna_lista_vazia():
    with patch("requests.get", side_effect=Exception("timeout")):
        result = _app.get_municipios.__wrapped__()
        assert result == []


# ── Testes de get_periodos ───────────────────────────────────────────────────

def test_get_periodos_sucesso():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "anos": [2023, 2022],
            "meses": ["2022-01", "2023-12"],
            "meses_por_ano": {"2022": ["2022-01"], "2023": ["2023-12"]},
        }
        mock_get.return_value.ok = True
        result = _app.get_periodos.__wrapped__()
        assert 2023 in result["anos"]


def test_get_periodos_falha_retorna_estrutura_vazia():
    with patch("requests.get", side_effect=ConnectionError()):
        result = _app.get_periodos.__wrapped__()
        assert result == {"anos": [], "meses": [], "meses_por_ano": {}}


# ── Testes de get_series ─────────────────────────────────────────────────────

def test_get_series_monta_params_corretos():
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = [{"municipio": "Curitiba / PR", "serie": []}]
        mock_get.return_value = mock_resp
        result = _app.get_series(["Curitiba / PR"], "2023-01", "2023-12", None)
        assert len(result) == 1
        assert result[0]["municipio"] == "Curitiba / PR"
        call_params = mock_get.call_args[1]["params"]
        assert "municipios" in call_params


def test_get_series_falha_retorna_lista_vazia():
    with patch("requests.get", side_effect=Exception()):
        assert _app.get_series(["SP"], None, None, None) == []


# ── Testes de criar_evento ───────────────────────────────────────────────────

def test_criar_evento_sucesso():
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"id": 1, "titulo": "Greve"}
        ok, err = _app.criar_evento({
            "titulo": "Greve",
            "descricao": "",
            "data_inicio": "2023-05-01",
            "data_fim": "2023-05-15",
            "impacto": "NEGATIVO",
        })
        assert ok is True
        assert err == ""


def test_criar_evento_falha_retorna_mensagem():
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {"detail": ["Título obrigatório"]}
        ok, err = _app.criar_evento({"titulo": ""})
        assert ok is False
        assert "Título" in err


def test_criar_evento_excecao_retorna_falso():
    with patch("requests.post", side_effect=ConnectionError("refused")):
        ok, err = _app.criar_evento({})
        assert ok is False


# ── Testes de excluir_evento ──────────────────────────────────────────────────

def test_excluir_evento_sucesso():
    with patch("requests.delete") as mock_del:
        mock_del.return_value.ok = True
        ok, err = _app.excluir_evento(1)
        assert ok is True


def test_excluir_evento_falha():
    with patch("requests.delete") as mock_del:
        mock_del.return_value.ok = False
        mock_del.return_value.text = "Not found"
        ok, err = _app.excluir_evento(999)
        assert ok is False


# ── Testes de atualizar_evento ────────────────────────────────────────────────

def test_atualizar_evento_sucesso():
    with patch("requests.put") as mock_put:
        mock_put.return_value.ok = True
        ok, err = _app.atualizar_evento(1, {"titulo": "Novo"})
        assert ok is True
        assert err == ""


def test_atualizar_evento_excecao():
    with patch("requests.put", side_effect=TimeoutError()):
        ok, err = _app.atualizar_evento(1, {})
        assert ok is False
