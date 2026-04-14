# 🏃 NoLimits Intelligence BI - Predição de Churn e Análise de Retenção

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

---

## 💡 Resumo do projeto

O **NoLimits Intelligence BI** é uma solução completa de Business Intelligence e Data Science desenvolvida para o CT de Corrida NoLimits. O sistema utiliza **Machine Learning** para prever o cancelamento de alunos (churn), um **Dashboard Interativo** para acompanhamento de KPIs financeiros e um **Assistente de IA Conversacional** que permite consultas ao banco de dados em linguagem natural. 

O projeto transforma dados brutos em decisões estratégicas, reduzindo a rotatividade e otimizando a receita do centro de treinamento.

---

## ❓ Problema de negócio / contexto

Centros de treinamento enfrentam um desafio constante: a **retenção de alunos**. A saída de um aluno não representa apenas uma perda de receita imediata, mas um aumento no custo de aquisição (CAC). 

**O desafio:** 
- Identificar padrões de comportamento que precedem o cancelamento.
- Automatizar a análise de saúde financeira (Faturamento e Ticket Médio).
- Facilitar o acesso aos dados para gestores que não dominam SQL.

---

## 📊 Dados utilizados

Os dados são armazenados em um banco de dados local **SQLite**, estruturado da seguinte forma:

| Tabela | Descrição |
|--------|-----------|
| `alunos` | Informações cadastrais de cada aluno. |
| `planos` | Detalhes dos planos (Standard, Premium, Ilimitado) e valores. |
| `vinculos` | Histórico de contratos, datas de início/fim e status (Ativo/Cancelado). |
| `dados_semana` | Registro detalhado de presenças (check-ins) para análise de frequência. |

> [!NOTE]
> Os dados originais são anonimizados via script (`anonimizar_dados.py`) para garantir a privacidade e segurança das informações.

---

## 🛠️ Metodologia e ferramentas

A solução foi construída em três camadas principais:

1.  **ETL e Análise (Python & SQL)**: Extração de dados do SQLite, limpeza com **Pandas** e monitoramento via **Pipeline de Produção** (`pipeline.py`).
2.  **Inteligência Preditiva (Machine Learning)**: Implementação de um modelo de **Regressão Logística** para prever o risco de churn baseado em *tenure* (tempo de casa) e frequência semanal.
3.  **Visualização e IA (Streamlit & LangChain)**: 
    *   Dashboard com KPIs financeiros dinâmicos.
    *   Chatbot RAG (Retrieval-Augmented Generation) para consultas em linguagem natural.

---

## 📈 Principais insights e resultados (Data Case)

Após a análise dos dados e execução do modelo, os seguintes resultados foram extraídos:

- **Taxa de Churn Geral**: **27.2%** (Identificado nos últimos 120 dias).
- **Fator de Risco Crítico**: Alunos com frequência menor que 2x/semana têm **2.3x mais chance** de cancelar.
- **Faturamento**: R$ 52.349,00 com um **Ticket Médio** de R$ 887,27.
- **Modelo de ML**: Acurácia de **88%** na predição de desertores.

> [!IMPORTANT]
> **Ação Recomendada**: Implementar um protocolo de "Onboarding Crítico" nos primeiros 45 dias de contrato para alunos com baixa frequência inicial. Veja mais em [`insights/acoes_estrategicas.md`](file:///home/igor/Documentos/GIT/NoLimitsBI/insights/acoes_estrategicas.md).

---

## 🚀 Como executar o projeto

### Pré-requisitos
- Python 3.9+
- [Ollama](https://ollama.ai/) instalado (com modelo `llama3.1` ou superior).

### Instalação
1. Clone o repositório e acesse a pasta.
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o Pipeline para preparar os modelos:
   ```bash
   python pipeline.py
   ```
5. Inicie a aplicação:
   ```bash
   streamlit run app.py
   ```

---

## 🤝 Contato

Desenvolvido por **Igor** – *Analista de Dados & Desenvolvedor*

- [Portfólio Pessoal](https://github.com/igortude)
- [LinkedIn](https://www.linkedin.com/in/seuconfirmar)
- [E-mail](mailto:seuemail@exemplo.com)

---
*Este projeto é uma prova técnica de ponta a ponta, unindo Engenharia de Dados, Analytics e Inteligência Artificial.*
