from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db' #URI do banco

db.init_app(app) #registrando no sqlalchemy a aplicação



with app.app_context():
    db.create_all()


@app.route('/')
def index():
    user = User(nome='Thiago')
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/listar')
def listar():
    sttm = db.select(User)
    print(sttm)
    #resultado = db.session.execute(db.select(User)).all()
    resultado = db.session.query(User).all()
    return render_template('listar.html', resultado=resultado)
