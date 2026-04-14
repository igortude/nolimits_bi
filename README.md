# 🏃 NoLimits BI - Centro de Treinamento

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

Uma solução de Business Intelligence robusta e inteligente desenvolvida para o **Centro de Treinamento de Corrida NoLimits**. O projeto unifica a visualização de métricas de negócios com um assistente de IA capaz de consultar dados em linguagem natural.

---

## 🚀 Funcionalidades Principais

### 1. 🤖 NoLimits IA (Assistente de Dados)
A joia da coroa do projeto. Utilizando **LangChain** e modelos **Llama 3.1 (via Ollama)**, o sistema permite consultas complexas ao banco de dados usando linguagem natural.
- **Conversão Natural-para-SQL**: Transforma perguntas como *"Quem são os alunos ativos do plano premium?"* em queries SQLite otimizadas.
- **Histórico de Interação**: Mantém o contexto das perguntas e permite navegação rápida por consultas anteriores.
- **Segurança**: Filtros rígidos impedem comandos de modificação (DROP, DELETE, UPDATE) via chat.

### 2. 📊 Painéis Interativos
- **Painel Geral**: Visão consolidada de métricas operacionais e fluxo de alunos.
- **Painel de Negócios**: Focado em saúde financeira, faturamentos e análise de planos.

### 3. 🎨 Visual Moderno
- Interface personalizada com **CSS customizado**.
- Tematização profissional alinhada à identidade visual do CT NoLimits.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend/Core**: [Streamlit](https://streamlit.io/)
- **Inteligência Artificial**: [LangChain](https://www.langchain.com/) + LLM Llama 3.1
- **Banco de Dados**: SQLite
- **Estilização**: CSS Customizado

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.9+
- [Ollama](https://ollama.ai/) instalado e rodando com o modelo `llama3.1`.

### Instruções
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/NoLimitsBI.git
   cd NoLimitsBI
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

---

## 🔒 Segurança e Anonimização (Preparação para GitHub)

Este projeto contém scripts para garantir que nenhum dado sensível dos alunos seja exposto publicamente.

### Scripts de Dados:
- **`anonimizar_dados.py`**: Gera uma cópia segura (`data/nolimits_ai_public.db`) substituindo nomes reais por pseudônimos (ex: `Aluno_001`). **Sempre execute este script antes de subir atualizações do banco.**
- **`seed_fake_data.py`**: Cria uma base de dados limpa com dados fictícios para fins de teste.

> [!IMPORTANT]
> O banco de dados original (`data/nolimits_ai.db`) está devidamente configurado no `.gitignore` e **nunca** deve ser submetido ao controle de versão.

---

## 📂 Estrutura do Projeto

```text
├── app.py              # Ponto de entrada (Streamlit)
├── app/                # Lógica de styles e assets
├── dashboard/          # Módulos das abas e painéis
├── data/               # Bancos de dados e scripts SQL
├── scripts_ia/         # Lógica e contextos da IA
├── anonimizar_dados.py # Script de segurança de dados
└── requirements.txt    # Dependências do projeto
```

---

## 👥 Desenvolvedores
- Igor
- Leonardo

---
*Este projeto foi desenvolvido para otimizar a gestão e análise de desempenho do CT NoLimits.*
