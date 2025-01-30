from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    rg = Column(String(20), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Produto(Base):
    __tablename__ = 'produto'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # vaso, planta, flor
    preco = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

class Compra(Base):
    __tablename__ = 'compra'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    data_pedido = Column(DateTime, nullable=False)
    produtos = relationship('Produto', secondary='compra_produto', backref='compras')

class CompraProduto(Base):
    __tablename__ = 'compra_produto'
    
    id = Column(Integer, primary_key=True)
    compra_id = Column(Integer, ForeignKey('compra.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)

# Configuração do banco de dados
engine = create_engine('sqlite:///florista.db')
Base.metadata.create_all(engine)

# Criação da sessão
Session = sessionmaker(bind=engine)
session = Session()