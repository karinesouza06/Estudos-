from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas no banco de dados
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)')
    conn.execute('CREATE TABLE IF NOT EXISTS veiculos (id INTEGER PRIMARY KEY AUTOINCREMENT, modelo TEXT NOT NULL, ano INTEGER NOT NULL, marca TEXT NOT NULL)')
    conn.execute('CREATE TABLE IF NOT EXISTS locacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, veiculo_id INTEGER, cliente_id INTEGER, data_locacao TEXT, FOREIGN KEY(veiculo_id) REFERENCES veiculos(id), FOREIGN KEY(cliente_id) REFERENCES clientes(id))')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    init_db()
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        return redirect('/cadastrar_cliente')
    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar_veiculo', methods=['GET', 'POST'])
def cadastrar_veiculo():
    init_db()
    if request.method == 'POST':
        modelo = request.form['modelo']
        ano = request.form['ano']
        marca = request.form['marca']
        conn = get_db_connection()
        conn.execute('INSERT INTO veiculos (modelo, ano, marca) VALUES (?, ?, ?)', (modelo, ano, marca))
        conn.commit()
        conn.close()
        return redirect('/cadastrar_veiculo')
    return render_template('cadastrar_veiculo.html')

@app.route('/cadastrar_locacao', methods=['GET', 'POST'])
def cadastrar_locacao():
    init_db()
    if request.method == 'POST':
        veiculo_id = request.form['veiculo_id']
        cliente_id = request.form['cliente_id']
        data_locacao = request.form['data_locacao']
        conn = get_db_connection()
        conn.execute('INSERT INTO locacoes (veiculo_id, cliente_id, data_locacao) VALUES (?, ?, ?)', (veiculo_id, cliente_id, data_locacao))
        conn.commit()
        conn.close()
        return redirect('/cadastrar_locacao')
    else:
        conn = get_db_connection()
        veiculos = conn.execute('SELECT * FROM veiculos').fetchall()
        clientes = conn.execute('SELECT * FROM clientes').fetchall()
        conn.close()
        return render_template('cadastrar_locacao.html', veiculos=veiculos, clientes=clientes)

@app.route('/lista_clientes')
def lista_clientes():
    init_db()
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/lista_veiculos')
def lista_veiculos():
    init_db()
    conn = get_db_connection()
    veiculos = conn.execute('SELECT * FROM veiculos').fetchall()
    conn.close()
    return render_template('lista_veiculos.html', veiculos=veiculos)

@app.route('/lista_locacoes')
def lista_locacoes():
    init_db()
    conn = get_db_connection()
    locacoes = conn.execute('SELECT locacoes.*, veiculos.modelo, clientes.nome FROM locacoes JOIN veiculos ON locacoes.veiculo_id = veiculos.id JOIN clientes ON locacoes.cliente_id = clientes.id').fetchall()
    conn.close()
    return render_template('lista_locacoes.html', locacoes=locacoes)