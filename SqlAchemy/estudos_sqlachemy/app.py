"""
ANOTAÇÕES
1 - instalar o sqlachemy (pip install sqlalchemy)
2 - importações (from sqlalchemy import create_engine(é o que vai criar ou conectar o banco))
3 - tudo que você for fazer no seu banco, é efeito dentro de uma sessão, que ao final você irá comita-lá.


case4 - github romerito (usar como base)
"""

from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base


db = create_engine("sqlite:///database.db")

Session = sessionmaker(bind=db) #bind é o parametro que diz qual o nome do banco
session = Session() #chama o Session que inicializa o banco

Base = declarative_base()
#aqui é onde deve criar as tabelas 
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column('id', Integer, primary_key=True, autoincrement=True) #cria uma coluna na qual o primeiro parametro é o nome do campo e o segundo é o tipo
    nome = Column('nome', String)
    email = Column('email', String)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)

    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo


class Livro(Base):
    __tablename__ = "livros"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    titulo = Column('titulo', String)
    qtde_paginas = Column('qtde_pagina', Integer)
    dono = Column('dono', ForeignKey('usuarios.id'))

    def __init__(self, titulo, qtde_paginas, dono):
        self.titulo = titulo
        self.qtde_paginas = qtde_paginas
        self.dono = dono


Base.metadata.create_all(bind=db) #vai criar todas as tabelas que estiverem dentro de db

#adiciona
usuario = Usuario(nome='micka2', email='micka2@gmail.com', senha='123')
session.add(usuario) #adiciona
session.commit() #salva



lista_usuarios = session.query(Usuario).all() #query permite fazer uma consulta no banco de acordo com a tabela especificada. '.all() -> retorna todos' ".fisrt() -> retorna o primeiro. "
print(lista_usuarios)  #-> retorna uma lista 

lista_usuario = session.query(Usuario).filter_by(email='micka2@gmail.com').first()


livro = Livro(titulo='Crepusculo', qtde_paginas='300', dono=lista_usuario.id)
session.add(livro)
session.commit()


#Update
lista_usuario.nome='Liana'
session.add(lista_usuario)
session.commit()

#delete
session.delete(lista_usuario)
session.commit()

