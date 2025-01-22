from sqlalchemy import create_engine 
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from typing import List

engine = create_engine('sqlite:///exemplo1.db')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass


estudante_curso = Table(
    "estudantes_cursos",
    Base.metadata,
    Column('estudantes_id', ForeignKey('estudantes.id'), primary_key=True),
    Column('curso_id', ForeignKey('cursos.id'), primary_key=True),
)


#relacionamento NxN
class Curso(Base):
    __tablename__ = 'cursos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    cursos: Mapped[List['Curso']] = relationship(
        'Curso', back_populates = 'estudante'
    )

    def __repr__(self) -> str:
        return f"Nome=({self.nome})"
   

class Estudante(Base):
    __tablename__ = 'estudantes'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] 

    estudantes: Mapped[List['Estudante']] = relationship(
        'Estudante', back_populates = 'curso'
    )
   
    def __repr__(self) -> str:
        return f"Nome=({self.nome})"

Base.metadata.create_all(bind=engine)