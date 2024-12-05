from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text 

app = Flask(__name__)

engine = create_engine("sqlite:///database.db")
connection = engine.connect()

tabela = text("""
   CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT NOT NULL 
   )
""")
       
connection.execute(tabela)
connection.commit()

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']


        user = text("""SELECT nome FROM users WHERE users.nome == :nome""")
        lista = connection.execute(user, {'nome':nome})




        if lista.first() == None:
            insert = text("""INSERT INTO users(nome) VALUES(:nome)""")
            connection.execute(insert, {'nome':nome})
            connection.commit()

            return render_template('index.html')
            
           

    return render_template('register.html')

