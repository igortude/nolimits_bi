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
        st.subheader("💰 Visão Financeira")

        faturamento = get_faturamento_total()
        ticket_medio = get_ticket_medio()

        c1, c2, c3 = st.columns(3)
        
        c1.metric(
            label="💵 FATURAMENTO TOTAL",
            value=f"R$ {faturamento:,.2f}"
        )

        c2.metric(
            label="🎟️ TICKET MÉDIO",
            value=f"R$ {ticket_medio:,.2f}"
        )

        c3.metric(
            label="📈 META MENSAL",
            value="105%",
            delta="Superado"
        )

    with tab_plan:
        st.subheader("📦 Planos & Receita")
        receitas_planos = get_receita_por_plano()
        
        cols = st.columns(len(receitas_planos)) if receitas_planos else [st.columns(1)]
        if receitas_planos:
            for i, (plano, rec) in enumerate(receitas_planos.items()):
                cols[i].metric(label=f"💎 {plano}", value=f"R$ {rec:,.2f}")
        else:
            st.info("Nenhuma receita encontrada para os planos.")

    with tab_risc:
        st.subheader("🔎 Riscos & Oportunidades")
        risco_churn = get_risco_financeiro_churn()
        
        c1, c2 = st.columns([1, 1.5])
        c1.metric("🔴 VALOR EM RISCO (CHURN)", f"R$ {risco_churn:,.2f}", delta="Atenção Crítica", delta_color="inverse")
        
        c2.warning("""
            **Análise de Risco:**
            Alunos com mais de 3 faltas consecutivas representam este montante. 
            Recomendamos o envio de mensagens personalizadas de "Sentimos sua falta".
        """)

    with tab_proj:
        st.subheader("🔮 Projeções Financeiras")
        fat_atual, risco, rec_projetada = get_dados_projecao()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Base", f"R$ {fat_atual:,.2f}")
        c2.metric("Perda Est. (Churn)", f"R$ {risco:,.2f}", delta_color="inverse")
        c3.metric("Receita Alvo", f"R$ {rec_projetada:,.2f}", delta="+5.0%")
        
        st.markdown("---")
        st.caption("Evolução projetada com base na retenção histórica e meta de crescimento orgânico.")