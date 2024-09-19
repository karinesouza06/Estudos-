from flask_login import UserMixin
import sqlite3

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


class User(UserMixin):
    id: str
    def __init__(self, matricula, email, senha):
        self.matricula = matricula
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, id):
        conn = obter_conexao()
        dados = conn.execute("SELECT * FROM usuarios WHERE id=(?)", (id,)).fetchone()
        conn.commit()
        conn.close()
        if dados:
            user = User(dados["matricula"], dados["email"], dados["senha"])
            user.id = dados["id"]
            return user
        else:
            return None