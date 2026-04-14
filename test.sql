-- Quais turnos existem em cada dia?
SELECT 
    ds.dia,
    COUNT(DISTINCT ds.turno) AS qtd_turnos
FROM dados_semana AS ds
JOIN alunos AS a ON a.nome = ds.aluno
JOIN vinculos AS v ON v.aluno_id = a.id
WHERE ds.turno IN ('matutino', 'vespertino')
--   AND v.status = 'ativo'
GROUP BY ds.dia
HAVING COUNT(DISTINCT ds.turno) = 2  -- AMBOS os turnos presentes
ORDER BY ds.dia DESC;


------------------------------------------------
SELECT COUNT(p.id) AS qt_alunos_mensal1x
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
where nome = 'Mensal 1x';

SELECT COUNT(p.id) as qt_alunos_mensal2x
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
where nome = 'Mensal 2x';

SELECT COUNT(p.id) as qt_alunos_mensal3x
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
where nome = 'Mensal 3x';

SELECT COUNT(p.id) as qt_alunos_mensal_ilmtd
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
where nome = 'Mensal Ilimitado';

-------------------------------------------------------------------------------
SELECT p.nome AS plano,
       COUNT(DISTINCT v.aluno_id) AS qtd
FROM vinculos v
JOIN planos p ON p.id = v.plano_id
WHERE p.nome IN ('Mensal 1x','Mensal 2x','Mensal 3x','Mensal Ilimitado')
GROUP BY p.nome;

-------------------------------------------------------------------------------
select ds.dia,
count(DISTINCT ds.turno) as qt_turnos
 from dados_semana AS ds
join alunos AS a on a.nome = ds.aluno
join vinculos as v on v.aluno_id = a.id
WHERE ds.turno in ('matutino', 'vespertino')
GROUP BY ds.dia
HAVING count(DISTINCT ds.turno) = 2
ORDER BY ds.dia desc
limit 1             -- data escolhida por ter aluno em ambos os turnos

SELECT 
COUNT(DISTINCT aluno)
from dados_semana
WHERE dia >= '2025-11-02'
AND dia <= '2025-11-28'
-- AND check_in = 'ausente'
and check_in = 'presente'   -- ALUNOS ATIVOS ÚLTIMAS 3 SEMANAS

SELECT COUNT(*)
FROM(
        SELECT aluno
        FROM dados_semana
        WHERE dia BETWEEN '2025-11-02' AND '2025-11-28'
        AND check_in = 'presente'
        GROUP BY aluno
        HAVING COUNT(*) >= 5
    ) as t      -- CONTA a subquery que lista os alunos dentro dos filtros

SELECT aluno 
, COUNT(aluno) AS qt_ausencia
from dados_semana
WHERE dia <= '2025-11-01' 
AND check_in = 'ausente'
GROUP BY aluno
ORDER BY COUNT(aluno) DESC
LIMIT 10

WITH ausencias AS (
    SELECT aluno, COUNT(*) AS qt_ausencia
    FROM dados_semana
    WHERE dia <= '2025-11-01'
      AND check_in = 'ausente'
    GROUP BY aluno
)
SELECT *
FROM ausencias
ORDER BY qt_ausencia DESC
LIMIT 10;
-- alunos ausentes no período do 'último mês'
-- considerando a

---- cálculo de médias por aluno (ausência)

WITH qt_faltas_por_aluno AS (
SELECT aluno, count(*) qt_faltas 
from dados_semana
WHERE dia <= '2025-11-28'
AND check_in = 'ausente'
group by aluno
)

select *
from qt_faltas_por_aluno
ORDER BY qt_faltas DESC

---- início das queries relacionadas ao plano_negocio.py

WITH rendNUM AS (
SELECT
p.nome
,COUNT(*) as clientsPlano
,p.preco_mensal
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
group by p.nome, p.preco_mensal
), -- qt de cliente por plano

ttpplano AS (
SELECT 
nome, 
clientsPlano * preco_mensal as valorporplano
FROM rendNUM    -- valor total por plano
),

totaldeclientes AS (
SELECT SUM(clientsPlano) AS total_clientes FROM rendNUM
)               -- valor total de clientes do studio

-- SELECT SUM(valorporplano) from ttpplano -- faturamento total

SELECT
nome
, clientsPlano
, ROUND(
clientsPlano * 100.0 / total_clientes ,2
) AS "%"
 FROM rendNUM
CROSS JOIN totaldeclientes on 1 = 1     -- porcentagem de alunos por plano




-------------------- MANIPULAÇÃO DO BANCO

--- Atualiazação do banco, para ter valores próximos do real

-- descobrir os ids de cada plano para atribuição de novos planos, considerando o cenário atual do studio

SELECT COUNT(*) as total_vinculos From vinculos;
SELECT * FROM PLANOS

/*
nome	        clientsPlano	preco_mensal
Mensal 1x	        3	        528.0
Mensal 2x	        48	        825.0
Mensal 3x	        28	        1012.0
Mensal Ilimitado	2	        1650.0
*/


WITH alunos_por_plano AS (
SELECT
p.nome
,COUNT(*) as clientsPlano
,p.preco_mensal
FROM vinculos as v
JOIN planos as p on p.id = v.plano_id
group by p.nome, p.preco_mensal
), -- qt de alunos por plano

ttpplano AS (
SELECT 
nome, 
clientsPlano * preco_mensal as valorporplano
FROM alunos_por_plano    -- valor total por plano
),

fat_total AS (
SELECT SUM(valorporplano) AS faturamento_total
from ttpplano -- faturamento total
),

total_alunos AS (
SELECT COUNT(DISTINCT aluno_id) AS total_alunos
from vinculos
)

SELECT
-- faturamento_total,
-- total_alunos, -- DESNECESSÁRIO, e também para não confundir na hora de passar o index na função. [2] ao invés de [0]
ROUND(faturamento_total * 1.0 / total_alunos,2) AS "Ticket Médio"
FROM fat_total, total_alunos --CROSSJOIN (produto cartesiano ... 1x1)
