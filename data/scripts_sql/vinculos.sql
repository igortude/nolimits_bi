DROP TABLE IF EXISTS vinculos;

CREATE TABLE vinculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    plano_id INTEGER,
    data_inicio DATE,
    data_fim DATE,
    status TEXT DEFAULT 'ativo',
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id)
);