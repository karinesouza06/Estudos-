
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True)
  email: Mapped[str]

  @classmethod
  def select_all(cls):
    users = db.session.execute(db.select(User)).scalars()
    return users
  
  @classmethod
  def insert(cls, user):
    db.session.add(user)
    db.session.commit()
  
  @classmethod
  def select_one(cls, id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    return user
  
  @classmethod
  def update(cls, email, id):
      user = User.select_one(id)
      user.email = email
      db.session.commit()
  

  
  





  

