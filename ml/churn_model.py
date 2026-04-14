import sqlite3
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, classification_report

DB_PATH = 'data/nolimits_ai.db'
MODEL_PATH = 'ml/churn_model.pkl'

def extract_features():
    conn = sqlite3.connect(DB_PATH)
    
    # Base query for students and their plans
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
    
    # Historical presence count
    freq_query = """
        SELECT 
            aluno as aluno_nome,
            COUNT(*) as total_presencas
        FROM dados_semana
        WHERE check_in = 'presente'
        GROUP BY aluno
    """
    df_freq = pd.read_sql_query(freq_query, conn)
    
    # Weekly average frequency (simulated by dividing total presences by estimated weeks)
    # Since it's a demo, we'll use total_presencas directly as a strong feature
    df = pd.merge(df, df_freq, on='aluno_nome', how='left').fillna(0)
    
    # Calculate Tenure (days)
    data_maxima = datetime(2025, 11, 28)
    
    def calc_tenure(row):
        start = datetime.strptime(row['data_inicio'], "%Y-%m-%d")
        if row['status'] == 'cancelado' and row['data_fim']:
            end = datetime.strptime(row['data_fim'], "%Y-%m-%d")
        else:
            end = data_maxima
        return max(1, (end - start).days)

    df['tenure'] = df.apply(calc_tenure, axis=1)
    df['is_churn'] = df['status'].apply(lambda x: 1 if x == 'cancelado' else 0)
    
    # Weekly average frequency feature
    df['freq_media_semanal'] = df['total_presencas'] / (df['tenure'] / 7.0)
    
    conn.close()
    return df

def train():
    print("Extracting features...")
    df = extract_features()
    
    # Features: tenure, frequency per week, plan value, plan frequency limit
    features = ['tenure', 'freq_media_semanal', 'preco_mensal', 'frequencia_semana']
    X = df[features]
    y = df['is_churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    
    print(f"Model Accuracy: {acc:.2%}")
    print(f"Model Recall (Churn): {rec:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature Importance
    importance = model.coef_[0]
    for i, v in enumerate(importance):
        print(f'Feature: {features[i]}, Score: {v:.5f}')
        
    # Save model
    os.makedirs('ml', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    return acc, rec

if __name__ == "__main__":
    train()
