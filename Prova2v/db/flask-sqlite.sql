CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exercicios (
    id_exercicios INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_ex TEXT NOT NULL,
    decricao TEXT
);



