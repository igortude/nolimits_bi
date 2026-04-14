import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'data/nolimits_ai.db'

def extract_ml_features():
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Base Query for Vinculos and Planos
    query = """
        SELECT 
            v.aluno_id,
            v.status,
            v.data_inicio,
            v.data_fim,
            p.preco_mensal,
            p.frequencia_semana,
            a.nome as aluno_nome
        FROM vinculos v
        JOIN planos p ON p.id = v.plano_id
        JOIN alunos a ON a.id = v.aluno_id
    """
    df = pd.read_sql_query(query, conn)
    
    # 2. Get Frequencies from dados_semana
    # Note: dados_semana uses names, so we use aluno_nome join or bridging via alunos table
    freq_query = """
        SELECT 
            aluno as aluno_nome,
            COUNT(*) as total_presencas
        FROM dados_semana
        WHERE check_in = 'presente'
        GROUP BY aluno
    """
    df_freq = pd.read_sql_query(freq_query, conn)
    
    # Merge
    df = pd.merge(df, df_freq, on='aluno_nome', how='left').fillna(0)
    
    # 3. Calculate Tenure
    data_maxima = datetime(2025, 11, 28) # Project context
    
    def calc_tenure(row):
        start = datetime.strptime(row['data_inicio'], "%Y-%m-%d")
        if row['status'] == 'cancelado' and row['data_fim']:
            end = datetime.strptime(row['data_fim'], "%Y-%m-%d")
        else:
            end = data_maxima
        return (end - start).days

    df['tenure'] = df.apply(calc_tenure, axis=1)
    df['is_churn'] = df['status'].apply(lambda x: 1 if x == 'cancelado' else 0)
    
    print("Features extracted (sample):")
    print(df[['aluno_id', 'is_churn', 'total_presencas', 'tenure', 'preco_mensal', 'frequencia_semana']].head())
    
    conn.close()

if __name__ == "__main__":
    extract_ml_features()
