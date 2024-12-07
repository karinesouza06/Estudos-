from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return "Bem-vindo ao Flask!"

@app.route('/sobre')
def sobre():
    return "Esta é a página Sobre"

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo ao Flask!"

#Desafio extra
@app.route('/contato')
def contato():
    mensagem = "É justo que muito custe aquilo que muito vale!"
    return mensagem