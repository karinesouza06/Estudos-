from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3, os.path
from models.users import User
from models.users import db

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.select_all()
    return render_template('pages/index.html', users=users)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        senha= request.form['password']

        if not email:
            flash('Email é obrigatório')
        else:
            user = User()
            user.email = email
            user.senha = senha
            User.insert(user)
            return redirect(url_for('index'))
    
    return render_template('pages/create.html')

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    
    user = User.select_one(id)

    if user == None:
        return redirect(url_for('error', message='Usuário Inexistente'))

    if request.method == 'POST':
        email = request.form['email']

        User.update(email, id)
        return redirect(url_for('index'))
    
    return render_template('pages/edit.html', user=user)

@app.route('/error')
def error():
    error = request.args.get('message')
    return render_template('errors/error.html', message=error)