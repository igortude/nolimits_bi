from data.database import get_connection
from datetime import timedelta, datetime


##############################################
# ÚLTIMA DATA VÁLIDA PARA A ANÁLISE
##############################################
# select ds.dia,
# count(DISTINCT ds.turno) as qt_turnos
#  from dados_semana AS ds
# join alunos AS a on a.nome = ds.aluno
# join vinculos as v on v.aluno_id = a.id
# WHERE ds.turno in ('matutino', 'vespertino')
# GROUP BY ds.dia
# HAVING count(DISTINCT ds.turno) = 2
# ORDER BY ds.dia desc
# limit 1

data_maxima = '2025-11-28'
data_inicio = '2025-11-03'
min_presencas = 5
###############################################

def get_total_alunos():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM alunos"
    cursor.execute(query)

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado

def get_alunos_ativos(data_maxima, semanas=3, min_presencas=5):
    conn = get_connection()
    cursor = conn.cursor()

    if isinstance(data_maxima, str):
        data_maxima = datetime.strptime(data_maxima, "%Y-%m-%d").date()

    data_inicio = data_maxima - timedelta(weeks=int(semanas))

    query = """
        SELECT COUNT(*)
        FROM (
            SELECT aluno
            FROM dados_semana
            WHERE dia BETWEEN ? AND ?
              AND check_in = 'presente'
            GROUP BY aluno
            HAVING COUNT(*) >= ?
        ) t
    """

    cursor.execute(
        query,
        (data_inicio, data_maxima, min_presencas)
    )

    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def get_alunos_ufreq15(data_maxima):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT COUNT(DISTINCT aluno) 
        FROM dados_semana
        WHERE dia >= DATE(?, '-15 days')
          AND dia <= ?
    """
    cursor.execute(query, (data_maxima, data_maxima))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def get_delta_ativos(data_maxima):
    # garante tipo date
    if isinstance(data_maxima, str):
        data_maxima = datetime.strptime(data_maxima, "%Y-%m-%d").date()

    data_mes_anterior = data_maxima - timedelta(days=30)

    ativos_atual = get_alunos_ativos(data_maxima)
    ativos_anterior = get_alunos_ativos(data_mes_anterior)

    return ativos_atual - ativos_anterior

def get_media_alunos():
    conn = get_connection()
    cursor = conn.cursor()

    query="""
        WITH presenca_diaria AS (
        SELECT  dia
                , COUNT(*) as qt_presentes
        FROM dados_semana
        
        WHERE check_in = 'presente'
        and dia <= ? 
        GROUP BY dia
    )

        SELECT ROUND(AVG(qt_presentes),1) AS media_presenca
        FROM presenca_diaria;
        """
    
    cursor.execute(query, (data_maxima,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def get_alunostop_10(data_maxima='2025-11-28'):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT aluno, COUNT(aluno) AS qt_presenca
        FROM dados_semana
        WHERE dia <= ?
          AND check_in = 'presente'
        GROUP BY aluno
        ORDER BY qt_presenca DESC
        LIMIT 10;
    """

    cursor.execute(query, (data_maxima,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def get_top10_ausencias():
    conn    =   get_connection()
    cursor  =   conn.cursor()

    query="""
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
    """

    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def get_alunos_por_plano():
    conn = get_connection()
    cursor = conn.cursor()

    planos_fixos = ["Mensal 1x", "Mensal 2x", "Mensal 3x", "Mensal Ilimitado"]
    placeholders = ",".join(["?"] * len(planos_fixos))

    query = f"""
        SELECT p.nome AS plano,
               COUNT(DISTINCT v.aluno_id) AS qtd
        FROM vinculos v
        JOIN planos p ON p.id = v.plano_id
        WHERE p.nome IN ({placeholders})
        GROUP BY p.nome;
    """

    cursor.execute(query, planos_fixos)
    rows = cursor.fetchall()
    conn.close()

    # garante sempre as 4 chaves, mesmo se algum plano vier zero
    resultado = {p: 0 for p in planos_fixos}
    for plano, qtd in rows:
        resultado[plano] = qtd

    return resultado