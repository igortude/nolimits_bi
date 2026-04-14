# 🧠 Ações Estratégicas - Retenção de Alunos

Baseado na análise de dados e no modelo preditivo de churn, as seguintes ações são recomendadas para otimizar a saúde do CT NoLimits.

---

## 1. ⚠️ Alerta de Baixa Frequência
**Problema:** Alunos que treinam menos de 2x por semana têm 2.3x mais chance de cancelar.
**Ação:**
- Disparar alerta automático no Dashboard para a recepção.
- Enviar mensagem personalizada via WhatsApp perguntando sobre os objetivos do aluno.

## 2. 🏁 Protocolo de Onboarding (Primeiros 45 dias)
**Problema:** O tempo médio até o cancelamento é de aproximadamente 80 dias para alunos que não se engajam.
**Ação:**
- Criar cronograma de acompanhamento semanal para novos alunos nas primeiras 6 semanas.
- Realizar uma "re-avaliação" gratuita no dia 30 para reforçar os ganhos.

## 3. 💎 Migração para Planos de Longo Prazo
**Problema:** O Plano Mensal Ilimitado apresenta a maior variabilidade de churn.
**Ação:**
- Oferecer descontos progressivos para migração para planos Trimestrais ou Semestrais.
- Focar no valor "comunidade" para os alunos do plano Standard.

## 4. 🔮 Predição Proativa
**Problema:** Esperar o aluno faltar por 15 dias é tarde demais.
**Ação:**
- Utilizar o modelo de Machine Learning (`ml/churn_model.pkl`) para identificar alunos no "limite" do risco antes mesmo de faltarem.

---

> [!TIP]
> **Raciocínio de Negócio**: O custo de aquisição (CAC) de um novo aluno é 5x maior que a manutenção de um atual. Focar em retenção é o caminho mais rápido para a lucratividade.
