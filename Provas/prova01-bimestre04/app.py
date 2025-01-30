from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cliente, Produto, Compra, CompraProduto
from datetime import datetime

app = Flask(__name__)
engine = create_engine('sqlite:///florista.db')
Base.metadata.create_all(engine)

# Criação da sessão
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        data = request.form
        novo_cliente = Cliente(rg=data['rg'], nome=data['nome'], telefone=data['telefone'])
        session.add(novo_cliente)
        session.commit()
        return redirect(url_for('listar_clientes'))
    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        data = request.form
        novo_produto = Produto(nome=data['nome'], tipo=data['tipo'], preco=data['preco'])
        session.add(novo_produto)
        session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('cadastrar_produto.html')

@app.route('/cadastrar_compra', methods=['GET', 'POST'])
def cadastrar_compra():
    if request.method == 'POST':
        data = request.form
        nova_compra = Compra(cliente_id=data['cliente_id'], data_pedido=datetime.now())
        session.add(nova_compra)
        session.commit()
        for produto_id in data.getlist('produtos'):
            compra_produto = CompraProduto(compra_id=nova_compra.id, produto_id=produto_id)
            session.add(compra_produto)
        session.commit()
        return redirect(url_for('listar_compras'))
    
    clientes = session.query(Cliente).all()
    produtos = session.query(Produto).all()
    return render_template('cadastrar_compra.html', clientes=clientes, produtos=produtos)

@app.route('/listar_clientes')
def listar_clientes():
    clientes = session.query(Cliente).all()
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/listar_produtos')
def listar_produtos():
    produtos = session.query(Produto).all()
    return render_template('listar_produtos.html', produtos=produtos)

@app.route('/compras', methods=['POST'])
def add_compra():
    data = request.get_json()
    nova_compra = Compra(cliente_id=data['cliente_id'], data_pedido=datetime.now())
    session.add(nova_compra)
    session.commit()
    for produto_id in data['produtos']:
        compra_produto = CompraProduto(compra_id=nova_compra.id, produto_id=produto_id)
        session.add(compra_produto)
    session.commit()
    return {"message": "Compra registrada!"}, 201


@app.route('/listar_compras')
def listar_compras():
    compras = session.query(Compra).all()
    result = []
    for compra in compras:
        # Obtenha o cliente correspondente
        cliente = session.query(Cliente).filter(Cliente.id == compra.cliente_id).first()
        
        # Obtenha os IDs dos produtos através da tabela associativa
        produtos_ids = [cp.produto_id for cp in session.query(CompraProduto).filter(CompraProduto.compra_id == compra.id).all()]
        
        # Obtenha os nomes dos produtos correspondentes
        produtos_nomes = [session.query(Produto).filter(Produto.id == produto_id).first().nome for produto_id in produtos_ids]

        result.append({
            'cliente_nome': cliente.nome,  # Adiciona o nome do cliente
            'data_pedido': compra.data_pedido,
            'produtos': produtos_nomes  # Adiciona os nomes dos produtos
        })
    return render_template('listar_compras.html', compras=result)