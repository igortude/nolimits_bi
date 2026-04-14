import streamlit as st
from pathlib import Path
from . import painel_geral, painel_negocios, painel_chat

# --------------------------------
# IMPORTAÇÃO DE CSS
# --------------------------------
CSS_PATH = Path(__file__).parent.parent / "app" / "styles" / "custom.css"

def load_css():
    if CSS_PATH.exists():
        with open(CSS_PATH) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Arquivo CSS não encontrado!")


# ================================
# TELA INICIAL / CONTROLE DE ACESSO
# ================================
def render_inicio():

    # Configuração da página (deve vir no topo)
    st.set_page_config(
        page_title="NoLimits - Centro de Treinamento",
        page_icon="💪",
        layout="wide"
    )

    load_css()

    # Estado de sessão
    if "acesso_liberado" not in st.session_state:
        st.session_state.acesso_liberado = False

    # ================================
    # LOGIN
    # ================================
    if not st.session_state.acesso_liberado:

        st.markdown(
            '<h1 class="header-inicial">NO Limits - Centro de Treinamento</h1>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<h5 class="inicial">Para acessar, é necessário informar seu nome</h5>',
            unsafe_allow_html=True
        )

        nome = st.text_input("Nome", key="nome_input", label_visibility="collapsed")
        nomes_permitidos = ["Igor", "Leonardo", "Leo"]

        if not nome:
            st.divider()
            st.info("Foram utilizados dados referentes ao último trimestre de 2025.")

        elif nome not in nomes_permitidos:
            st.error(
                f"🔒 Acesso negado, {nome}. "
                "Entre em contato com o responsável."
            )

        else:
            st.success(f"🔓 Acesso liberado, {nome}!")
            st.session_state.acesso_liberado = True
            st.rerun()

        # 🔴 Impede QUALQUER coisa abaixo de renderizar
        st.stop()

    # ================================
    # DASHBOARD (SÓ APÓS LOGIN)
    # ================================
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

    tab_geral, tab_negocios, tab_ia = st.tabs(
        ["📊 Painel Geral", "💼 Negócios", "🔍 Consulta IA"]
    )

    with tab_geral:
        painel_geral.render()

    with tab_negocios:
        painel_negocios.render()

    with tab_ia:
        painel_chat.render()

    st.markdown('</div>', unsafe_allow_html=True)
