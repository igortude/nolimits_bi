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
            WHERE v.status = 'ativo'
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
                p.nome,
                COUNT(*) as clientsPlano,
                p.preco_mensal
            FROM vinculos as v
            JOIN planos as p on p.id = v.plano_id
            WHERE v.status = 'ativo'
            group by p.nome, p.preco_mensal
        ),
        ttpplano AS (
            SELECT 
                nome, 
                clientsPlano * preco_mensal as valorporplano
            FROM alunos_por_plano
        ),
        fat_total AS (
            SELECT SUM(valorporplano) AS faturamento_total
            from ttpplano
        ),
        total_alunos AS (
            SELECT COUNT(DISTINCT aluno_id) AS total_alunos
            from vinculos
            WHERE status = 'ativo'
        )
        SELECT
            ROUND(faturamento_total * 1.0 / total_alunos, 2) AS "Ticket Médio"
        FROM fat_total, total_alunos
    """)
    valor = cur.fetchone()[0]
    conn.close()

    return valor or 0

def get_receita_por_plano():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.nome,
            SUM(p.preco_mensal) AS receita_total
        FROM vinculos v
        JOIN planos p ON p.id = v.plano_id
        WHERE v.status = 'ativo'
        GROUP BY p.nome
        ORDER BY receita_total DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return {row[0]: row[1] or 0 for row in rows}

def get_risco_financeiro_churn():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        WITH ausencias AS (
            SELECT aluno, COUNT(*) AS qt_ausencia
            FROM dados_semana
            WHERE dia <= '2025-11-28'
            AND check_in = 'ausente'
            GROUP BY aluno
            HAVING qt_ausencia >= 3
        ),
        alunos_risco AS (
            SELECT a.id, p.preco_mensal
            FROM ausencias au
            JOIN alunos a ON a.nome = au.aluno
            JOIN vinculos v ON v.aluno_id = a.id
            JOIN planos p ON p.id = v.plano_id
            WHERE v.status = 'ativo'
        )
        SELECT SUM(preco_mensal) FROM alunos_risco
    """)

    valor = cur.fetchone()[0]
    conn.close()

    return valor or 0

def get_dados_projecao():
    faturamento_atual = get_faturamento_total()
    risco = get_risco_financeiro_churn()
    
    receita_projetada = (faturamento_atual * 1.05) - risco
    return faturamento_atual, risco, receita_projetada

def get_churn_rate():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            (COUNT(*) FILTER (WHERE status = 'cancelado') * 100.0 / COUNT(*)) AS churn_rate
        FROM vinculos
    """)
    rate = cur.fetchone()[0]
    conn.close()
    return rate or 0

def get_tempo_medio_cancelamento():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            AVG(julianday(data_fim) - julianday(data_inicio)) AS tempo_medio
        FROM vinculos
        WHERE status = 'cancelado'
    """)
    tempo = cur.fetchone()[0]
    conn.close()
    return tempo or 0

def get_frequencia_vs_churn():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            v.status,
            AVG(presencas_cont) as media_freq
        FROM (
            SELECT aluno, COUNT(*) as presencas_cont
            FROM dados_semana
            WHERE check_in = 'presente'
            GROUP BY aluno
        ) as ps
        JOIN alunos a ON a.nome = ps.aluno
        JOIN vinculos v ON v.aluno_id = a.id
        GROUP BY v.status
    """)
    rows = cur.fetchall()
    conn.close()
    return dict(rows)