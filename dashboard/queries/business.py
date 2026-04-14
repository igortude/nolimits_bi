from data.database import get_connection

def get_faturamento_total():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        WITH rendNUM AS (
            SELECT
                p.nome,
                COUNT(*) AS clientsPlano,
                p.preco_mensal
            FROM vinculos v
            JOIN planos p ON p.id = v.plano_id
            GROUP BY p.nome, p.preco_mensal
        ),
        ttpplano AS (
            SELECT clientsPlano * preco_mensal AS valorporplano
            FROM rendNUM
        )
        SELECT SUM(valorporplano) FROM ttpplano
    """)

    valor = cur.fetchone()[0]
    conn.close()

    return valor or 0

def get_ticket_medio ():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
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
        ROUND(faturamento_total * 1.0 / total_alunos,2) AS "Ticket Médio"
        FROM fat_total, total_alunos
            """)
    valor = cur.fetchone()[0]
    conn.close()

    return valor or 0