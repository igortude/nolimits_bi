# app/gerar_vinculos.py
import sqlite3, random, datetime

conn = sqlite3.connect("data/nolimits_ai.db")
cur = conn.cursor()

alunos = [r[0] for r in cur.execute("SELECT id FROM alunos").fetchall()]
for aid in alunos:
    pid = random.randint(1, 4)  # um dos 4 planos
    inicio = datetime.date(2025, 8, random.randint(1, 28))
    fim = inicio + datetime.timedelta(days=random.choice([90, 180, 365]))  # 3,6,12 meses
    cur.execute("""
        INSERT INTO vinculos (aluno_id, plano_id, data_inicio, data_fim)
        VALUES (?, ?, ?, ?)
    """, (aid, pid, inicio, fim))

conn.commit()
conn.close()
print("✅ Vínculos criados.")