DROP TABLE IF EXISTS planos;

CREATE TABLE planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    frequencia_semana INTEGER,
    preco_mensal REAL,
    periodo TEXT DEFAULT 'mensal'
);

INSERT INTO planos (nome, frequencia_semana, preco_mensal, periodo) VALUES
('Mensal 1x', 1, 528.00, 'mensal'),
('Mensal 2x', 2, 825.00, 'mensal'),
('Mensal 3x', 3, 1012.00, 'mensal'),
('Mensal Ilimitado', 0, 1650.00, 'mensal');