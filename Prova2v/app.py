from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
from arquivo import User

from flask_login import LoginManager, login_user, login_required, logout_user  #tem que dá o pip install no flask_login
login_manager = LoginManager() #cria uma variável que está chamando a classe 'LoginManager()' que gerencia autênticação de usuários


app = Flask(__name__)


#Inicializa o LoginManager com a instância da aplicação Flask (app)
login_manager.init_app(app)  


#defini uma chave secreta para a criptografia de cookies na sessão 
app.config['SECRET_KEY'] = 'naotafacilromerito'

@login_manager.user_loader
def load_user(user_id):
 return User.get(user_id)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template ('login.html')
    
    else:
        #email = request.form['email']
        id = request.form['id']
        senha = request.form['senha']

        conn = obter_conexao()
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = (?)', (id,)).fetchone()
        #senha_user = conn.execute('SELECT senha FROM usuarios WHERE email = (?)', (email,)).fetchone()
        #user = conn.execute('SELECT * FROM usuarios').fetchone()
        conn.commit()

        if usuario and usuario['senha'] == senha:
            user = User(usuario["id"], usuario["email"], usuario["senha"])
            user.id = usuario["id"]
            login_user(user)
            return redirect(url_for('cadastro_exercicios')) 
        
        else:
            return redirect(url_for('cadastro'))


#quando usar um forms, com um method especificado, fazer esse if da linha 31.
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == 'GET':
        return render_template ('cadastro.html')
    
    else:
        #pegando os dados do forms de cadastro.
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        conn = obter_conexao()
        user = conn.execute('SELECT nome FROM usuarios WHERE email = (?)', (email,)).fetchone()
        conn.commit()
        
        # se tem usuário é pq ele existe e já está cadastrado.
        if user:
            # a função "url_for" gera uma url para a rota(nesse caso a função login e não o route) espeficicada, e o redirect redireciona para a url apresentada.
            return redirect(url_for('login')) 
        
        else:
            conn.execute('INSERT INTO usuarios (nome, senha, email) VALUES (?, ?, ?)', (nome, senha, email,)).fetchone()
            mat = conn.execute('SELECT nome, id FROM usuarios WHERE email = (?)', (email,)).fetchone()
            usuarios = [dict(mat)]
            conn.commit()
            conn.close()

            return render_template('index.html', teste=usuarios)

            #return redirect(url_for('login'))  #vai redirecionar para a página login para colocar seu nome e senha e verificar se realmente foi cadastrado.

@login_manager.user_loader
@app.route('/cadastro_exercicios')
@login_required  #apenas usuários logados pode acessar esta rota.
def cadastro_exercicios():

    if request.method == 'GET':
        return render_template ('cadastro-exercicios.html')
    else:

        nome_exercicio = request.form['nome_ex']
        descricao_exercicio = request.form['descricao_ex']
        id_user = request.form['id']

        conn = obter_conexao()
        #user = conn.execute('SELECT nome FROM usuarios WHERE email = (?)', (email,)).fetchone()
        conn.commit()




  


