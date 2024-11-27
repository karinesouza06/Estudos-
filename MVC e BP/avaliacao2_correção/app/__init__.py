from flask import Flask, render_template, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user
from users import users
from books import books
from auth.bp import login_manager



from auth import bp

app = Flask(__name__, template_folder='templates')
login = login_manager.init_app(app)



app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'


app.register_blueprint(users.bp)
app.register_blueprint(books.bp)
app.register_blueprint(bp.bp)


@app.route('/')
def index():
    return render_template('layout.html')