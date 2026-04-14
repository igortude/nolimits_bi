import sqlite3
import os
from datetime import datetime

DB_PATH = 'data/nolimits_ai_public.db'

def seed():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        print(f"Populando banco de dados clean: {DB_PATH}")

        # Criar tabelas se não existirem
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                frequencia_semana INTEGER,
                preco_mensal REAL,
                periodo TEXT DEFAULT 'mensal'
            )
        ''')

        # Inserir dados de exemplo (limpar antes para evitar duplicatas em seeds repetidos)
        cursor.execute("DELETE FROM alunos")
        cursor.execute("DELETE FROM planos")

        alunos_exemplo = [
            ("Aluno_001",),
            ("Aluno_002",),
            ("Aluno_003",),
        ]
        cursor.executemany("INSERT INTO alunos (nome) VALUES (?)", alunos_exemplo)

        planos_exemplo = [
            ("Plano Standard", 3, 150.0),
            ("Plano Premium", 5, 250.0),
        ]
        cursor.executemany("INSERT INTO planos (nome, frequencia_semana, preco_mensal) VALUES (?, ?, ?)", planos_exemplo)

        conn.commit()
        print("Seed finalizado com sucesso!")

    except Exception as e:
        print(f"Erro no seed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
