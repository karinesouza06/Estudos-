from flask import Flask, render_template, make_response, request, session, redirect
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def criar_cookie():

    resposta = make_response("O cookie foi criado")
    resposta.set_cookie("nome_usuario", "Lira")
    resposta.set_cookie("idade", "29")
    return resposta
   

    
@app.route("/ver-cookie")
def ver_cookie():
    cookies = request.cookies
    return cookies

#------------------------------------------------------------
# USANDO O FLASK-SESSION

@app.route("/index")
def index():
    if not session.get("name"):
        return redirect("/login")
    
    return render_template('index.html')
  
  
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
     
        return redirect("/index")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

