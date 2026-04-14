import streamlit as st
import pandas as pd
import plotly.express as px
from .queries.alunos import (
    get_total_alunos,
    get_alunos_ativos,
    get_alunos_ufreq15,
    get_media_alunos,
    get_alunostop_10,
    get_top10_ausencias,
    get_alunos_por_plano,
    get_delta_ativos,
    data_maxima
)

def render():
    st.markdown(
        """
        <div style="display:flex; justify-content:center; margin: 6px 0 10px 0;">
            <img class="header-logo" src="https://via.placeholder.com/240x90?text=LOGO" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("📊 NoLimits DashBoard")
    
    # Uso de Tabs para separar o "Bom" do "Preocupante"
    tab_geral, tab_alerta = st.tabs(["📈 Engajamento", "⚠️ Atenção / Churn"])

    with tab_geral:
        render_cards_positivos()
        st.subheader("🏆 Top 10 Presenças")
        render_grafico_presencas()
        st.subheader("📦 Alunos por Plano")
        render_cards_planos()
    
    with tab_alerta:
        render_cards_negativos()
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🚩 Alunos Ausentes")
            render_grafico_ausencias()
        with col2:
            st.subheader("💡 Sugestão de Ação")
            st.info("""
                **Lista de Recuperação:**
                - Enviar WhatsApp para o Top 3 ausentes.
                - Verificar se houve lesão ou problema financeiro.
                - Oferecer desconto em plano 'maior'.
            """)

total_alunos = get_total_alunos()
a_ativos = get_alunos_ativos(data_maxima)
delta_ativos = get_delta_ativos(data_maxima)
freq15 = get_alunos_ufreq15(data_maxima)
media_alunos =  get_media_alunos()

def render_cards_positivos():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Alunos", total_alunos)
    col2.metric("Ativos", a_ativos, delta=f"{delta_ativos:+d} // mês anterior")
    col3.metric("Frequentes (15d)", freq15)
    col4.metric("Média Diária", f"{media_alunos:.1f}")

def render_grafico_presencas():
    top10 = get_alunostop_10(data_maxima)
    if not top10:
        st.warning("Sem dados.")
        return

    nomes, presencas = zip(*top10)
    df = pd.DataFrame({"Aluno": nomes, "Presenças": presencas})
    
    fig = px.bar(
        df, x="Presenças", y="Aluno", orientation='h',
        text="Presenças", color="Presenças",
        color_continuous_scale="Greens", # Tons de verde
        height=400
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        coloraxis_showscale=False, # Remove a barra lateral para limpar o visual
        margin=dict(l=0, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_cards_negativos():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Exemplo de cálculo: se 10 alunos sumiram de 100, risco é 10%
    top10_ausentes = get_top10_ausencias()
    total_ativos = get_alunos_ativos(data_maxima)
    risco_churn = (len(top10_ausentes) / total_ativos * 100) if total_ativos > 0 else 0

    col1.empty()
    col2.metric("Risco de Perda (Alunos)", len(top10_ausentes), delta="Atenção", delta_color="inverse")
    col3.metric("% Risco de Churn", f"{risco_churn:.1f}%", delta="Crítico", delta_color="inverse")
    col4.metric("Média Faltas (Top 10)", "criar_função") # Exemplo estático
    col5.empty()

def render_grafico_ausencias():
    top10 = get_top10_ausencias()
    if not top10:
        st.info("Nenhum aluno com faltas críticas.")
        return

    nomes, faltas = zip(*top10)
    df = pd.DataFrame({"Aluno": nomes, "Faltas": faltas})

    # Usando escala de Vermelho/Laranja para indicar problema
    fig = px.bar(
        df, x="Faltas", y="Aluno", orientation="h",
        text="Faltas", color="Faltas",
        color_continuous_scale="Reds", 
        height=400
    )
    
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False, # Remove a barra lateral
        margin=dict(l=0, r=10, t=10, b=10)
    )
    
    fig.update_traces(marker_line_color='rgb(150,0,0)', marker_line_width=1.5)
    
    st.plotly_chart(fig, use_container_width=True, key="grafico_ausencias")

def render_cards_planos():
    planos = get_alunos_por_plano()  # esperado: dict {"Mensal 1x": 10, ...}

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mensal 1x", planos.get("Mensal 1x", 0))
    col2.metric("Mensal 2x", planos.get("Mensal 2x", 0))
    col3.metric("Mensal 3x", planos.get("Mensal 3x", 0))
    col4.metric("Mensal Ilimitado", planos.get("Mensal Ilimitado", 0))