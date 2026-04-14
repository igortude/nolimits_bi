import streamlit as st
from dashboard.queries.business import (
    get_faturamento_total,
    get_ticket_medio,
    get_receita_por_plano,
    get_risco_financeiro_churn,
    get_dados_projecao
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
        receitas_planos = get_receita_por_plano()
        if receitas_planos:
            for plano, rec in receitas_planos.items():
                st.metric(label=f"Receita - {plano}", value=f"R$ {rec:,.2f}")
        else:
            st.info("Nenhuma receita encontrada para os planos.")

    with tab_risc:
        st.subheader("Riscos & Oportunidades")
        risco_churn = get_risco_financeiro_churn()
        
        c1, c2 = st.columns(2)
        c1.metric("Valor em Risco (Churn Real)", f"R$ {risco_churn:,.2f}", delta="Atenção: alunos com +3 faltas", delta_color="inverse")
        
        c2.info("Este valor representa o faturamento projetado comprometido por alunos que apresentam alto risco de cancelamento dado o ritmo de ausências.")

    with tab_proj:
        st.subheader("Projeções Financeiras")
        fat_atual, risco, rec_projetada = get_dados_projecao()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Atual", f"R$ {fat_atual:,.2f}")
        c2.metric("Risco Identificado", f"R$ {risco:,.2f}", delta="- Perdas Evitáveis", delta_color="inverse")
        c3.metric("Projeção Conservadora", f"R$ {rec_projetada:,.2f}", delta="+5% Meta de Expansão", delta_color="normal")
        
        st.caption("A projeção considera a meta de +5% de expansão de plano somado com perdas prováveis em churn (alunos inativos ou alto índice de ausências).")