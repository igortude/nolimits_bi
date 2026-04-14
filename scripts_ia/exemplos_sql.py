# scripts_ia/exemplos_sql.py

def obter_todos_exemplos() -> str:
    """
    Exemplos críticos para o modelo gerar SQL válido no SQLite.
    Quanto mais exemplos certos, melhor ele acerta.
    """
    return """
EXEMPLOS DE PERGUNTAS E SQL CORRETO PARA O BANCO NOLIMITS (SQLite):

"Quais são os planos disponíveis?"
SELECT nome, frequencia_semana, preco_mensal FROM planos ORDER BY preco_mensal;

"Mostrar todos os planos com preço"
SELECT 
    nome || ' (' || frequencia_semana || 'x por semana)' AS plano,
    'R$ ' || REPLACE(CAST(preco_mensal AS TEXT), '.', ',') AS preco
FROM planos 
ORDER BY preco_mensal;

"Quantos alunos ativos?"
SELECT COUNT(*) FROM vinculos WHERE status = 'ativo';

"Qual o faturamento mensal atual?"
SELECT COALESCE(SUM(p.preco_mensal), 0) AS faturamento
FROM vinculos v
JOIN planos p ON v.plano_id = p.id
WHERE v.status = 'ativo';

"Alunos com mais faltas na última semana"
SELECT aluno, COUNT(*) AS faltas
FROM dados_semana
WHERE date(data_criacao) >= date('now', '-7 days')
  AND check_in = 'pendente'
GROUP BY aluno
ORDER BY faltas DESC
LIMIT 10;

"Taxa de presença nos últimos 7 dias"
SELECT 
    ROUND(100.0 * COUNT(CASE WHEN check_in = 'presente' THEN 1 END) / 
          NULLIF(COUNT(CASE WHEN check_in IN ('presente', 'ausente') THEN 1 END), 0), 1) 
    || '%' AS taxa_presenca
FROM dados_semana
WHERE date(data_criacao) >= date('now', '-7 days');

"Top 10 alunos mais presentes essa semana"
SELECT aluno, COUNT(*) AS presencas
FROM dados_semana
WHERE check_in = 'presente'
  AND date(data_criacao) >= date('now', '-7 days')
GROUP BY aluno
ORDER BY presencas DESC
LIMIT 10;

"Alunos que não vieram nem uma vez essa semana (e estão ativos)"
SELECT a.nome
FROM alunos a
WHERE EXISTS (SELECT 1 FROM vinculos v WHERE v.aluno_id = a.id AND v.status = 'ativo')
  AND NOT EXISTS (
    SELECT 1 FROM dados_semana ds 
    WHERE ds.aluno_id = a.id 
      AND ds.check_in = 'presente'
      AND date(ds.data_criacao) >= date('now', '-7 days')
  );

"Check-ins por dia da semana essa semana"
SELECT 
    CASE strftime('%w', data_criacao)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda' 
        WHEN '2' THEN 'Terça'
        WHEN '3' THEN 'Quarta'
        WHEN '4' THEN 'Quinta'
        WHEN '5' THEN 'Sexta'
        WHEN '6' THEN 'Sábado'
    END AS dia,
    COUNT(*) AS checkins
FROM dados_semana
WHERE date(data_criacao) >= date('now', '-7 days')
GROUP BY strftime('%w', data_criacao)
ORDER BY checkins DESC;

"Quantos alunos por plano?"
SELECT p.nome, COUNT(v.aluno_id) AS alunos
FROM planos p
LEFT JOIN vinculos v ON p.id = v.plano_id AND v.status = 'ativo'
GROUP BY p.id, p.nome
ORDER BY alunos DESC;
""".strip()