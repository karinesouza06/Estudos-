import sqlite3

# abre conexão
conn = sqlite3.connect('database.db')

try:
    with open("database/schema.sql") as f:
        conn.executescript(f.read())
except FileNotFoundError:
    print("O arquivo schema.sql não foi encontrado.")

# encerra operações
conn.commit()
conn.close()