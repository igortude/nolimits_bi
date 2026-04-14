import streamlit as st
from dashboard.queries.business import (
    get_faturamento_total,
    get_ticket_medio
)

def render():
    st.subheader("💼 Painel de Negócios")
    st.divider()

    tab_fin, tab_plan, tab_risc, tab_proj = st.tabs(
        ["💰 Visão Financeira", "📦 Planos & Receita", "🔎 Riscos&Oportunidades", "🔮 Projeções"]
    )

    with tab_fin:
        st.subheader("Visão Financeira")

        faturamento = get_faturamento_total()
        ticket_medio = get_ticket_medio()

        c1, c2, c3, c4 = st.columns(4)
        
        c1.empty()

        c2.metric(
            label="Faturamento Total",
            value=f"R$ {faturamento:,.2f}"
        )

        c3.metric(
            label="Ticket Médio",
            value=f"R$ {ticket_medio:,.2f}"
        )

        c4.empty()

    with tab_plan:
        st.subheader("Planos & Receita")

    with tab_risc:
        st.subheader("Riscos&Oportunidades")

    with tab_proj:
        st.subheader("Construção")