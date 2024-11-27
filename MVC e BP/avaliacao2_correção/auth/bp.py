
from flask import Flask, render_template, url_for, request, Blueprint, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from database import get_connection


from users.models import User
from books.models import Book


bp = Blueprint(name='auth_bp', import_name= __name__, url_prefix='/auth', template_folder = 'templates')


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']  

        conn = get_connection()
        usuario = conn.execute("SELECT * from users where email = ? and nome = ?", (email, nome,)).fetchone()
        conn.commit()

        #foi acrescentado as linhas 38(usuario = User.find(email=email)) e 40(login_user(usuario)).
        usuario = User.find(email=email)
        if usuario:
            login_user(usuario)
            return redirect(url_for('users.index'))
        
        else:
            return redirect(url_for('users.register'))
     
    return render_template("login.html")
        

@bp.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



