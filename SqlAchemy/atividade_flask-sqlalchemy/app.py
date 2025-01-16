from flask import Flask, render_template, request, redirect, url_for
from database.banco import db, User, Book


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        nome= request.form['nome']

        user = User(nome=nome)
        db.session.add(user)
        db.session.commit()

        pessoas = db.session.query(User).all()
        liv = db.session.query(Book).all()
        return render_template('listar.html', pessoas=pessoas, liv=liv)
    return render_template('usuarios.html')


@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'POST':
        titulo= request.form['titulo']
        autor = request.form['autor']

        dados = Book(titulo=titulo, autor=autor)
        db.session.add(dados)
        db.session.commit()

        pessoas = db.session.query(User).all()
        liv = db.session.query(Book).all()
        return render_template('listar.html', liv=liv, pessoas=pessoas)
    return render_template('livro.html')

@app.route('/listar')
def listar():
    return render_template('listar.html')
    