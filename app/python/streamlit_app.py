"""Painel Analítico – Cesta Básica  |  Streamlit Frontend"""
from __future__ import annotations

import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime

API = "http://localhost:8000/api"

st.set_page_config(
    page_title="Painel Cesta Básica",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 1.6rem; }
.card-verde  [data-testid="stMetricValue"] { color: #22c55e; }
.card-vermelho [data-testid="stMetricValue"] { color: #ef4444; }
.card-azul   [data-testid="stMetricValue"] { color: #3b82f6; }
.card-amarelo [data-testid="stMetricValue"] { color: #f59e0b; }
div[data-testid="stSidebar"] { background-color: #0f172a; }
div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers de API ───────────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def get_municipios() -> list[str]:
    try:
        return requests.get(f"{API}/municipios", timeout=5).json()
    except Exception:
        return []


@st.cache_data(ttl=300, show_spinner=False)
def get_periodos() -> dict:
    try:
        return requests.get(f"{API}/periodos", timeout=5).json()
    except Exception:
        return {"anos": [], "meses": [], "meses_por_ano": {}}


def get_series(municipios: list[str], mes_inicio: str | None, mes_fim: str | None, ano: int | None) -> list:
    params: dict = {}
    for m in municipios:
        params.setdefault("municipios", [])
        params["municipios"].append(m)  # type: ignore[union-attr]
    if mes_inicio:
        params["mes_inicio"] = mes_inicio
    if mes_fim:
        params["mes_fim"] = mes_fim
    if ano:
        params["ano_referencia"] = ano
    try:
        resp = requests.get(f"{API}/evolucao/series", params=params, timeout=10)
        return resp.json() if resp.ok else []
    except Exception:
        return []


def get_indicadores(municipios: list[str], mes_inicio: str | None, mes_fim: str | None, ano: int | None) -> dict:
    params: dict = {}
    for m in municipios:
        params.setdefault("municipios", [])
        params["municipios"].append(m)  # type: ignore[union-attr]
    if mes_inicio:
        params["mes_inicio"] = mes_inicio
    if mes_fim:
        params["mes_fim"] = mes_fim
    if ano:
        params["ano_referencia"] = ano
    try:
        resp = requests.get(f"{API}/evolucao/indicadores", params=params, timeout=10)
        return resp.json() if resp.ok else {}
    except Exception:
        return {}


def get_peso(municipios: list[str], mes_inicio: str | None, mes_fim: str | None, ano: int | None) -> list:
    params: dict = {}
    for m in municipios:
        params.setdefault("municipios", [])
        params["municipios"].append(m)  # type: ignore[union-attr]
    if mes_inicio:
        params["mes_inicio"] = mes_inicio
    if mes_fim:
        params["mes_fim"] = mes_fim
    if ano:
        params["ano_referencia"] = ano
    try:
        resp = requests.get(f"{API}/evolucao/peso-componentes", params=params, timeout=10)
        return resp.json() if resp.ok else []
    except Exception:
        return []


def get_eventos(inicio: date | None = None, fim: date | None = None) -> list:
    params = {}
    if inicio:
        params["inicio"] = inicio.isoformat()
    if fim:
        params["fim"] = fim.isoformat()
    try:
        resp = requests.get(f"{API}/eventos", params=params, timeout=5)
        return resp.json() if resp.ok else []
    except Exception:
        return []


def criar_evento(payload: dict) -> tuple[bool, str]:
    try:
        resp = requests.post(f"{API}/eventos", json=payload, timeout=5)
        if resp.ok:
            return True, ""
        detail = resp.json().get("detail", resp.text)
        if isinstance(detail, list):
            detail = "; ".join(detail)
        return False, detail
    except Exception as e:
        return False, str(e)


def atualizar_evento(evento_id: int, payload: dict) -> tuple[bool, str]:
    try:
        resp = requests.put(f"{API}/eventos/{evento_id}", json=payload, timeout=5)
        if resp.ok:
            return True, ""
        detail = resp.json().get("detail", resp.text)
        if isinstance(detail, list):
            detail = "; ".join(detail)
        return False, detail
    except Exception as e:
        return False, str(e)


def excluir_evento(evento_id: int) -> tuple[bool, str]:
    try:
        resp = requests.delete(f"{API}/eventos/{evento_id}", timeout=5)
        return resp.ok, "" if resp.ok else resp.text
    except Exception as e:
        return False, str(e)


# ── Sidebar ──────────────────────────────────────────────────────────────────

def sidebar_filtros():
    with st.sidebar:
        st.title("🛒 Cesta Básica")
        st.caption("Painel Analítico DIEESE")
        st.divider()

        municipios_disponiveis = get_municipios()
        periodos = get_periodos()
        anos_disponiveis: list[int] = periodos.get("anos", [])
        meses_disponiveis: list[str] = periodos.get("meses", [])

        padroes = [m for m in ["São Paulo / SP", "Rio de Janeiro / RJ", "Brasília / DF"] if m in municipios_disponiveis]
        municipios_sel: list[str] = st.multiselect(
            "Municípios",
            options=municipios_disponiveis,
            default=padroes or municipios_disponiveis[:3],
            help="Selecione um ou mais municípios",
        )

        st.markdown("**Período**")
        col1, col2 = st.columns(2)
        mes_inicio_sel = col1.selectbox("De", options=[""] + meses_disponiveis, index=0, label_visibility="collapsed")
        mes_fim_sel = col2.selectbox("Até", options=[""] + meses_disponiveis, index=0, label_visibility="collapsed")

        ano_sel = st.selectbox(
            "Ano de referência",
            options=[None] + anos_disponiveis,
            format_func=lambda x: "Todos os anos" if x is None else str(x),
        )

        st.divider()
        pagina = st.radio(
            "Navegação",
            ["📈 Evolução", "📊 Indicadores", "🥩 Componentes", "📅 Eventos"],
            label_visibility="collapsed",
        )

        if not municipios_disponiveis:
            st.warning("API indisponível ou sem dados.")

    return (
        municipios_sel,
        mes_inicio_sel or None,
        mes_fim_sel or None,
        ano_sel,
        pagina,
    )


# ── Página: Evolução ─────────────────────────────────────────────────────────

def pagina_evolucao(municipios, mes_inicio, mes_fim, ano):
    st.header("📈 Evolução do Preço da Cesta Básica")

    if not municipios:
        st.info("Selecione ao menos um município na barra lateral.")
        return

    with st.spinner("Carregando dados..."):
        series = get_series(municipios, mes_inicio, mes_fim, ano)

    if not series:
        st.warning("Sem dados para os filtros selecionados.")
        return

    fig = go.Figure()
    for s in series:
        nome = s["municipio"]
        meses = [p["mes"] for p in s["serie"]]
        valores = [p["cesta"] for p in s["serie"]]
        fig.add_trace(go.Scatter(
            x=meses, y=valores, mode="lines+markers",
            name=nome, hovertemplate="%{x}<br>R$ %{y:.2f}<extra>" + nome + "</extra>",
        ))

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Valor Total (R$)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0),
        height=460,
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font_color="#e2e8f0",
        xaxis=dict(gridcolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabela resumo
    with st.expander("Ver tabela de dados"):
        for s in series:
            st.markdown(f"**{s['municipio']}**")
            rows = [{"Mês": p["mes"], "Total (R$)": f"R$ {p['cesta']:.2f}"} for p in s["serie"]]
            st.dataframe(rows, use_container_width=True, hide_index=True)


# ── Página: Indicadores ───────────────────────────────────────────────────────

def pagina_indicadores(municipios, mes_inicio, mes_fim, ano):
    st.header("📊 Indicadores")

    if not municipios:
        st.info("Selecione ao menos um município na barra lateral.")
        return

    with st.spinner("Calculando indicadores..."):
        ind = get_indicadores(municipios, mes_inicio, mes_fim, ano)

    if not ind:
        st.warning("Sem dados para os filtros selecionados.")
        return

    col1, col2, col3, col4 = st.columns(4)

    # Menor preço
    mp = ind.get("menor_preco")
    with col1:
        if mp:
            st.metric(
                label="🏷️ Menor Preço",
                value=f"R$ {mp['valor']:,.2f}",
                help=mp.get("observacao", ""),
            )
            st.caption(mp.get("observacao", ""))
        else:
            st.metric("🏷️ Menor Preço", "—")

    # Variação mensal
    vm = ind.get("variacao_mensal")
    with col2:
        if vm and vm.get("percentual") is not None:
            pct = vm["percentual"]
            delta_str = f"{'+' if pct >= 0 else ''}{pct:.1f}%"
            st.metric("📅 Var. Mensal", delta_str, delta=delta_str)
            st.caption(f"{vm['municipios_considerados']} municípios")
        else:
            st.metric("📅 Var. Mensal", "—")

    # Variação anual
    va = ind.get("variacao_anual")
    with col3:
        if va and va.get("percentual") is not None:
            pct = va["percentual"]
            delta_str = f"{'+' if pct >= 0 else ''}{pct:.1f}%"
            st.metric("📆 Var. Anual", delta_str, delta=delta_str)
            st.caption(f"{va['municipios_considerados']} municípios")
        else:
            st.metric("📆 Var. Anual", "—")

    # Tendência
    tend = ind.get("tendencia")
    with col4:
        if tend:
            icone = {"ALTA": "🔺", "QUEDA": "🔻", "ESTAVEL": "➡️"}.get(tend["status"], "❓")
            st.metric(f"{icone} Tendência", tend["texto"])
            st.caption(tend.get("descricao", ""))
        else:
            st.metric("❓ Tendência", "—")


# ── Página: Componentes ───────────────────────────────────────────────────────

_NOMES_PT = {
    "carne": "Carne", "leite": "Leite", "feijao": "Feijão",
    "arroz": "Arroz", "farinha": "Farinha", "batata": "Batata",
    "tomate": "Tomate", "pao": "Pão", "cafe": "Café",
    "banana": "Banana", "acucar": "Açúcar", "oleo": "Óleo",
    "manteiga": "Manteiga",
}


def pagina_componentes(municipios, mes_inicio, mes_fim, ano):
    st.header("🥩 Peso dos Componentes")

    if not municipios:
        st.info("Selecione ao menos um município na barra lateral.")
        return

    with st.spinner("Calculando composição..."):
        pesos = get_peso(municipios, mes_inicio, mes_fim, ano)

    if not pesos:
        st.warning("Sem dados para os filtros selecionados.")
        return

    tabs = st.tabs([p["rotulo"] for p in pesos])
    for tab, mun in zip(tabs, pesos):
        with tab:
            comps = mun["componentes"]
            if not comps:
                st.info("Sem dados de componentes.")
                continue

            labels = [_NOMES_PT.get(c["chave"], c["chave"]) for c in comps]
            medias = [c["media"] for c in comps]
            pcts = [c["percentual"] for c in comps]

            col_pizza, col_barra = st.columns([1, 1])

            with col_pizza:
                fig_pie = go.Figure(go.Pie(
                    labels=labels, values=pcts,
                    hole=0.4,
                    textinfo="label+percent",
                    hovertemplate="%{label}<br>Média: R$ %{customdata:.2f}<br>%{percent}<extra></extra>",
                    customdata=medias,
                ))
                fig_pie.update_layout(
                    showlegend=False, height=380,
                    plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", font_color="#e2e8f0",
                    margin=dict(l=0, r=0, t=20, b=0),
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_barra:
                fig_bar = go.Figure(go.Bar(
                    x=labels, y=medias,
                    text=[f"R$ {v:.2f}" for v in medias],
                    textposition="outside",
                    marker_color=px.colors.qualitative.Set3[:len(labels)],
                ))
                fig_bar.update_layout(
                    yaxis_title="Média R$", height=380,
                    plot_bgcolor="#0f172a", paper_bgcolor="#0f172a", font_color="#e2e8f0",
                    xaxis=dict(gridcolor="#1e293b"),
                    yaxis=dict(gridcolor="#1e293b"),
                    margin=dict(l=0, r=0, t=20, b=0),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # Destaques
            d = mun.get("destaques")
            if d:
                st.subheader("Destaques")
                dc1, dc2, dc3, dc4 = st.columns(4)
                def _fmt_destaque(item):
                    if not item:
                        return "—", ""
                    nome = _NOMES_PT.get(item["chave"], item["chave"])
                    return f"R$ {item['media']:.2f}", nome
                v, n = _fmt_destaque(d.get("item_mais_caro"))
                dc1.metric("💰 Mais caro", v, help=n)
                dc1.caption(n)
                v, n = _fmt_destaque(d.get("item_mais_barato"))
                dc2.metric("🪙 Mais barato", v, help=n)
                dc2.caption(n)
                ia = d.get("maior_aumento")
                if ia and ia.get("variacao") is not None:
                    dc3.metric("📈 Maior alta", f"+{ia['variacao']:.1f}%")
                    dc3.caption(_NOMES_PT.get(ia["chave"], ia["chave"]))
                ir = d.get("maior_reducao")
                if ir and ir.get("variacao") is not None:
                    dc4.metric("📉 Maior queda", f"{ir['variacao']:.1f}%")
                    dc4.caption(_NOMES_PT.get(ir["chave"], ir["chave"]))

            # Tabela detalhada
            with st.expander("Ver tabela detalhada"):
                rows = []
                for c in comps:
                    rows.append({
                        "Componente": _NOMES_PT.get(c["chave"], c["chave"]),
                        "Média (R$)": f"R$ {c['media']:.2f}",
                        "% do total": f"{c['percentual']:.1f}%",
                        "Variação": f"{c['variacao']:+.1f}%" if c.get("variacao") is not None else "—",
                        "Início": c.get("mes_inicial", "—"),
                        "Fim": c.get("mes_final", "—"),
                    })
                st.dataframe(rows, use_container_width=True, hide_index=True)


# ── Página: Eventos ───────────────────────────────────────────────────────────

def pagina_eventos():
    st.header("📅 Eventos Externos")
    st.caption("Registre eventos que impactaram o preço da cesta básica.")

    # Formulário de criação / edição
    with st.expander("➕ Novo Evento", expanded=False):
        _form_evento()

    st.divider()

    eventos = get_eventos()
    if not eventos:
        st.info("Nenhum evento cadastrado.")
        return

    # Lista
    for ev in eventos:
        impacto_cor = "🟢" if ev["impacto"] == "POSITIVO" else "🔴"
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.markdown(f"**{ev['titulo']}** {impacto_cor}")
                st.caption(ev.get("descricao", "") or "")
            with c2:
                st.markdown(f"`{ev['periodo_inicio']}` → `{ev['periodo_fim']}`")
            with c3:
                col_edit, col_del = st.columns(2)
                if col_edit.button("✏️", key=f"edit_{ev['id']}", help="Editar"):
                    st.session_state[f"edit_open_{ev['id']}"] = True
                if col_del.button("🗑️", key=f"del_{ev['id']}", help="Excluir"):
                    ok, err = excluir_evento(ev["id"])
                    if ok:
                        st.success("Evento excluído.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Erro: {err}")

            if st.session_state.get(f"edit_open_{ev['id']}"):
                _form_evento(ev)


def _form_evento(ev: dict | None = None):
    is_edit = ev is not None
    prefix = f"ev_{ev['id']}_" if is_edit else "novo_"

    with st.form(key=f"form_{prefix}"):
        titulo = st.text_input("Título *", value=ev["titulo"] if is_edit else "")
        descricao = st.text_area("Descrição", value=ev.get("descricao", "") if is_edit else "", height=80)

        col1, col2, col3 = st.columns(3)
        di_default = date.fromisoformat(ev["data_inicio"]) if is_edit else date.today()
        df_default = date.fromisoformat(ev["data_fim"]) if is_edit else date.today()
        data_inicio = col1.date_input("Data início *", value=di_default)
        data_fim = col2.date_input("Data fim *", value=df_default)
        impacto = col3.selectbox(
            "Impacto *",
            ["NEGATIVO", "POSITIVO"],
            index=0 if not is_edit else (0 if ev["impacto"] == "NEGATIVO" else 1),
        )

        label = "💾 Salvar alterações" if is_edit else "✅ Criar evento"
        submitted = st.form_submit_button(label, use_container_width=True)
        if submitted:
            if not titulo.strip():
                st.error("Título é obrigatório.")
            elif data_fim < data_inicio:
                st.error("Data fim deve ser >= data início.")
            else:
                payload = {
                    "titulo": titulo.strip(),
                    "descricao": descricao.strip(),
                    "data_inicio": data_inicio.isoformat(),
                    "data_fim": data_fim.isoformat(),
                    "impacto": impacto,
                }
                if is_edit:
                    ok, err = atualizar_evento(ev["id"], payload)
                else:
                    ok, err = criar_evento(payload)

                if ok:
                    st.success("Salvo com sucesso!")
                    if is_edit:
                        st.session_state[f"edit_open_{ev['id']}"] = False
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Erro: {err}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    municipios, mes_inicio, mes_fim, ano, pagina = sidebar_filtros()

    if pagina == "📈 Evolução":
        pagina_evolucao(municipios, mes_inicio, mes_fim, ano)
    elif pagina == "📊 Indicadores":
        pagina_indicadores(municipios, mes_inicio, mes_fim, ano)
    elif pagina == "🥩 Componentes":
        pagina_componentes(municipios, mes_inicio, mes_fim, ano)
    elif pagina == "📅 Eventos":
        pagina_eventos()


if __name__ == "__main__":
    main()
