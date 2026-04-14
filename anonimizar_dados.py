import sqlite3
import shutil
import os

# Configurações
DB_ORIGINAL = 'data/nolimits_ai.db'
DB_PUBLICO = 'data/nolimits_ai_public.db'

def anonimizar():
    # 1. Garantir que o diretório de destino existe
    os.makedirs(os.path.dirname(DB_PUBLICO), exist_ok=True)

    # 2. Criar uma cópia do banco original
    print(f"Copiando {DB_ORIGINAL} para {DB_PUBLICO}...")
    shutil.copy2(DB_ORIGINAL, DB_PUBLICO)

    # 3. Conectar ao banco público
    conn = sqlite3.connect(DB_PUBLICO)
    cursor = conn.cursor()

    try:
        print("Iniciando processo de anonimização...")

        # Mapeamento para garantir consistência entre tabelas
        # { 'Nome Real': 'Aluno_001' }
        mapeamento_nomes = {}
        contador = 1

        # --- A. Processar tabela 'alunos' ---
        cursor.execute("SELECT id, nome FROM alunos")
        alunos = cursor.fetchall()
        
        for aluno_id, nome_real in alunos:
            if nome_real not in mapeamento_nomes:
                pseudonimo = f"Aluno_{contador:03d}"
                mapeamento_nomes[nome_real] = pseudonimo
                contador += 1
            
            cursor.execute(
                "UPDATE alunos SET nome = ? WHERE id = ?",
                (mapeamento_nomes[nome_real], aluno_id)
            )

        print(f"Tabela 'alunos' anonimizada ({len(alunos)} registros).")

        # --- B. Processar tabela 'dados_semana' ---
        # Verificando se a tabela existe antes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados_semana'")
        if cursor.fetchone():
            cursor.execute("SELECT id, aluno FROM dados_semana")
            dados = cursor.fetchall()
            
            for registro_id, nome_real in dados:
                if nome_real:
                    # Se o nome não estiver no mapeamento ainda, cria um novo pseudônimo
                    if nome_real not in mapeamento_nomes:
                        pseudonimo = f"Aluno_{contador:03d}"
                        mapeamento_nomes[nome_real] = pseudonimo
                        contador += 1
                    
                    cursor.execute(
                        "UPDATE dados_semana SET aluno = ? WHERE id = ?",
                        (mapeamento_nomes[nome_real], registro_id)
                    )
            print(f"Tabela 'dados_semana' anonimizada ({len(dados)} registros).")

        conn.commit()
        print("\nSucesso! O banco público foi gerado e anonimizado.")
        print(f"Arquivo gerado: {DB_PUBLICO}")

    except Exception as e:
        conn.rollback()
        print(f"Erro durante a anonimização: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DB_ORIGINAL):
        print(f"Erro: O arquivo {DB_ORIGINAL} não foi encontrado.")
    else:
        anonimizar()
