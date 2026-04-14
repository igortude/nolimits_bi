# 🧠 NoLimits Intelligence Dashboard 💪  
### Aplicação de IA e Análise de Negócios com Streamlit + SQLite + LangChain + Ollama

---

## 🚀 Sobre o Projeto
O **NoLimits Intelligence Dashboard** nasceu como um estudo real aplicado ao ambiente de uma academia/studio de personal training.  
O objetivo é unir **visão de negócio**, **análise de dados** e **inteligência artificial local** em uma única aplicação web.

A aplicação oferece:
- 📊 **Dashboard interativo** com métricas financeiras e operacionais  
- 💬 **Chat IA** que compreende perguntas em linguagem natural e responde com base nas tabelas do banco de dados real  
- ⚙️ Execução 100% local, utilizando **Ollama** (com modelos LLaMA 3, DeepSeek, Mistral etc.)  

---

## 🧱 Arquitetura Geral


---

## 🧩 Stack de Tecnologias
| Camada | Ferramenta | Função |
|---------|-------------|--------|
| **Frontend / UI** | [Streamlit](https://streamlit.io) | Interface web do dashboard e chat |
| **Banco de dados** | [SQLite](https://sqlite.org) | Armazena alunos, planos, presenças |
| **Análise de dados** | Pandas + Altair | Consultas SQL → DataFrames → Gráficos |
| **IA Local** | [Ollama](https://ollama.ai) + LangChain | Interpretação de linguagem natural e geração/executação de SQL |
| **Modelo LLM** | LLaMA 3 / DeepSeek / Mistral | Engine de respostas locais offline |

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório

git clone https://github.com/SEU_USUARIO/MyBusiness_AI.git
cd MyBusiness_AI

### 2️⃣ Criar e ativar o ambiente virtual Python
```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# ou:
venv\Scripts\activate          # Windows

```
### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt

```
### 4️⃣ Verificar se o Ollama está ativo e baixar o modelo
```bash
ollama list       # confirma se mistral, llama3.2 ou deepseek estão disponíveis
ollama pull llama3.2

```

### 5️⃣ Executar a aplicação
```
streamlit run app/dashboard.py

```

Abra o link exibido (geralmente http://localhost:8501)
e explore:

Abas Dashboard → gráficos e métricas,
Abas Chat Inteligente → assistente IA consultando dados reais.

🧠 O que o Dashboard mostra
* Receita mensal por plano (1x, 2x, 3x, Ilimitado)
* Top 10 alunos por frequência
* Gráficos Altair + tabelas (Pandas)
* Integração dinâmica com banco SQLite


#####
#####
##### GRAFICO
#####
#####


💬 O Assistente de Negócios
Na aba Chat Inteligente:
```bash
Você pode fazer perguntas como
text

Quantos alunos existem?
Quantos alunos estão no plano Mensal 3x?
Qual aluno é mais rentável?
O modelo LLM transforma a pergunta em SQL válida, executa no SQLite e responde em tempo real.
Totalmente offline com Ollama (local LLM).

```

> O modelo LLM transforma a pergunta em SQL válida, executa no SQLite e responde em tempo real.
> Totalmente offline com Ollama (local LLM).

🧰 Principais componentes do código

Arquivo	Propósito
dashboard.py	Junta dashboard e chat, gera consultas, conecta ao Ollama
gerar_vinculos.py	Popula a tabela de vínculos aluno↔plano
scripts_sql/	Contém arquivos .sql (',CREATE TABLE ...') para recriar o banco
~/.streamlit/config.toml	Define tema dark e cores da interface

🧠 Conceitos LangChain empregados
ChatOllama → modelo local carregado via Ollama
SQLDatabase → interface de conexão com SQLite
SQLDatabaseSequentialChain → gera SQL ⇢ executa ⇢ sintetiza resposta
PromptTemplate → define o formato da pergunta enviada ao modelo

📈 Evoluções planejadas
Adicionar mais visuais (Altair/Plotly) para análises por mês e turno
Integrar memória de conversa no chat (ConversationBufferMemory)
Implementar alertas/insights preditivos via Machine Learning (local)
Deploy 📤 no Streamlit Community Cloud com README interativo

