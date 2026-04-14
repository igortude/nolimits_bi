# dashboard/painel_chat.py

import streamlit as st
from pathlib import Path

# LangChain
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Seus módulos
from scripts_ia import CONTEXTO_NOLIMITS, CORRECOES_AUTOMATICAS
from scripts_ia.exemplos_sql import obter_todos_exemplos

# ================================================================
# CONFIGURAÇÃO
# ================================================================

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "nolimits_ai.db"
DATABASE_URI = f"sqlite:///{DB_PATH}"

MODELO_SQL = "llama3.1"
MODELO_HUMANO = "llama3.1"

# ================================================================
# CONEXÕES CACHEADAS (OBRIGATÓRIO TER @st.cache_resource)
# ================================================================

@st.cache_resource
def conectar_banco():
    return SQLDatabase.from_uri(DATABASE_URI)

@st.cache_resource
def carregar_llm_sql():
    return ChatOllama(model=MODELO_SQL, temperature=0)

@st.cache_resource
def carregar_llm_humano():
    return ChatOllama(model=MODELO_HUMANO, temperature=0.7)

# ================================================================
# PROMPTS
# ================================================================

PROMPT_SQL = ChatPromptTemplate.from_messages([
    ("system", """Você é um especialista em SQL para o banco SQLite do NoLimits CT de Corrida.

REGRAS OBRIGATÓRIAS:
1. Use apenas sintaxe válida do SQLite
2. Para datas: use date('now', '-7 days'), date('now', '-30 days')
3. Use COALESCE() e NULLIF() quando necessário
4. Use strftime('%w', campo) para dia da semana
5. Retorne APENAS o SQL limpo, sem ```sql nem explicações

Schema completo do banco:
{schema}

EXEMPLOS QUE FUNCIONAM 100% NO NOSSO BANCO:
{exemplos_sql}
"""),
    ("human", "{pergunta}")
])

PROMPT_RESPOSTA = ChatPromptTemplate.from_messages([
    ("system", f"""Você é o assistente oficial do NoLimits CT.

{CONTEXTO_NOLIMITS}

REGRAS RÍGIDAS E COMPORTAMENTO HUMANO:
- Seja extremamente empático, amigável e focado na jornada do(a) gestor(a) do NoLimits.
- Inicie a resposta sempre com uma saudação calorosa (se for a primeira frase) e utilize emojis (🥊, 💪, 🥋, 🔥).
- NUNCA aja como um robô que apenas lê dados ou linhas de banco.
- Transforme os dados em observações construtivas e conversas em tom humano. Exemplo: "Opa, que ótimo número! Temos atualmente 81 guerreiros treinando com a gente! 💪"
- Nunca invente valores, nomes de planos ou preços. Se não encontrar, peça desculpas com empatia ("Poxa, ainda não encontrei essa informação nos registros 😅").
- Use SOMENTE os dados que aparecerem no resultado do SQL.
- Formate dinheiro como R$ 1.234,56.

Exemplo de boa resposta:
"Aí sim! 🎉 Os planos disponíveis para nossos atletas são:
• Mensal 3x/semana - O favorito por R$ 390,00 🚀
• Mensal 2x/semana - R$ 290,00
• Mensal 1x/semana - R$ 170,00"

Site: www.ctnolimits.com.br
"""),
    ("human", """Pergunta: {pergunta}
SQL: {sql}
Resultado: {resultado}

Responda com base APENAS nesses dados:""")
])

# ================================================================
# FUNÇÕES AUXILIARES
# ================================================================

def limpar_sql(sql: str) -> str:
    sql = sql.strip()
    if "```" in sql:
        sql = "\n".join(l for l in sql.split("\n") if not l.strip().startswith("```"))
    return sql.replace(";", "").strip()

def validar_sql(sql: str) -> bool:
    proibidos = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE"]
    return not any(p in sql.upper() for p in proibidos)

def corrigir_resposta(txt: str) -> str:
    for errado, certo in CORRECOES_AUTOMATICAS.items():
        txt = txt.replace(errado, certo)
        txt = txt.replace(errado.title(), certo)
        txt = txt.replace(errado.upper(), certo.upper())
    txt = txt.replace("nolimits", "NoLimits").replace("No limits", "NoLimits")
    return txt

# ================================================================
# FUNÇÃO PRINCIPAL
# ================================================================

def perguntar(pergunta: str) -> dict:
    try:
        db = conectar_banco()
        llm_sql = carregar_llm_sql()
        llm_humano = carregar_llm_humano()

        # Geração do SQL com exemplos corretos
        chain_sql = PROMPT_SQL | llm_sql | StrOutputParser()
        sql_bruto = chain_sql.invoke({
            "schema": db.get_table_info(),
            "exemplos_sql": obter_todos_exemplos(),
            "pergunta": pergunta
        })
        sql = limpar_sql(sql_bruto)

        if not validar_sql(sql):
            return {"resposta": "Só faço consultas de leitura.", "sql": sql, "erro": True}

        try:
            resultado = db.run(sql)
        except Exception as e:
            return {"resposta": f"Erro na consulta:\n{str(e)}", "sql": sql, "erro": True}

        chain_resposta = PROMPT_RESPOSTA | llm_humano | StrOutputParser()
        resposta_bruta = chain_resposta.invoke({
            "pergunta": pergunta,
            "sql": sql,
            "resultado": resultado or "Nenhum resultado."
        })

        return {
            "resposta": corrigir_resposta(resposta_bruta),
            "sql": sql,
            "resultado": resultado,
            "erro": False
        }

    except Exception as e:
        return {"resposta": f"Erro interno: {str(e)}", "erro": True}

# ================================================================
# INTERFACE
# ================================================================

def render():
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="margin-bottom: 0;">🤖 NoLimits IA</h1>
            <p style="color: #94a3b8; font-size: 1.1rem;">Especialista em Performance & Dados do CT</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Inicializa histórico
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "pergunta_selecionada" not in st.session_state:
        st.session_state.pergunta_selecionada = None

    # ================================================================
    # SIDEBAR COM HISTÓRICO CLICÁVEL
    # ================================================================
    with st.sidebar:
        st.markdown("# NoLimits CT")
        st.markdown("**[www.ctnolimits.com.br](https://www.ctnolimits.com.br)**")
        st.markdown("---")
        st.markdown("### Histórico de Perguntas")

        if st.session_state.historico:
            # Mostra apenas as perguntas do usuário
            perguntas = [
                msg for msg in st.session_state.historico 
                if msg["role"] == "user"
            ]
            for i, msg in enumerate(perguntas):
                indice_real = st.session_state.historico.index(msg)
                pergunta_curta = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                
                if st.button(
                    f"{i+1}. {pergunta_curta}",
                    key=f"btn_{indice_real}",
                    use_container_width=True
                ):
                    st.session_state.pergunta_selecionada = indice_real
        else:
            st.info("Nenhuma pergunta ainda. Comece perguntando!")

    # ================================================================
    # CHAT PRINCIPAL
    # ================================================================

    # Se o usuário clicou em uma pergunta do histórico
    if st.session_state.pergunta_selecionada is not None:
        idx = st.session_state.pergunta_selecionada
        if idx < len(st.session_state.historico):
            msg_pergunta = st.session_state.historico[idx]
            msg_resposta = st.session_state.historico[idx + 1] if idx + 1 < len(st.session_state.historico) else None

            with st.chat_message("user"):
                st.markdown(msg_pergunta["content"])

            with st.chat_message("assistant"):
                st.markdown(msg_resposta["content"] if msg_resposta else "Resposta não encontrada.")
                if msg_resposta and msg_resposta.get("sql"):
                    with st.expander("Ver SQL gerado"):
                        st.code(msg_resposta["sql"], language="sql")
        else:
            st.info("Pergunta não encontrada.")
    else:
        # Mostra o histórico completo normalmente
        for msg in st.session_state.historico:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sql"):
                    with st.expander("Ver SQL"):
                        st.code(msg["sql"], language="sql")

    # ================================================================
    # INPUT NOVA PERGUNTA
    # ================================================================
    if prompt := st.chat_input("Digite sua pergunta aqui..."):
        # Adiciona pergunta
        st.session_state.historico.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gera resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                resp = perguntar(prompt)
            st.markdown(resp["resposta"])
            if resp.get("sql"):
                with st.expander("Ver SQL"):
                    st.code(resp["sql"], language="sql")

        # Salva resposta
        st.session_state.historico.append({
            "role": "assistant",
            "content": resp["resposta"],
            "sql": resp.get("sql", "")
        })

        # Limpa seleção para não travar na pergunta antiga
        st.session_state.pergunta_selecionada = None
        st.rerun()