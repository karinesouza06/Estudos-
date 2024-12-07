from flask import Flask, request, render_template, session, redirect, url_for, make_response
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave-secreta' #necessário para gerenciar sessões

# obtém conexão com o banco de dados
def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE email = (?)", (username,)).fetchone()
          
        # Verificar se o usuário já está logado
        if user :
            return redirect(url_for('dashboard'))
        else:
            return render_template('cadastro.html', mensagem=f'Olá, {username}. Você não está cadastrado, portanto, cadastre-se!')

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE email = (?)", (username,)).fetchone()

        if not user:
            conn.execute("INSERT INTO users(email, senha) VALUES (?,?)", (username, password)).fetchall()
            conn.commit()
            conn.close()
            session['username'] = username
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)
            return resposta
        else:
            return render_template('login.html', erro='Usuário já existente.')
    return render_template('cadastro.html')
    
    
@app.route('/dashboard')
def dashboard():
    # Verificar se o usuário está na sessão
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

@app.route('/logout', methods=['POST'])
def logout():
# Remover usuário da sessão
    session.pop('username', None)
    # Remover o cookie
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0) # Excluir o cookie
    return resposta