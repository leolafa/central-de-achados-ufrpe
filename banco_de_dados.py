#Importações necessarias
#Usando sqlalchemy como banco de dados
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base,relationship
from sqlalchemy import select
from datetime import datetime

#configuraçoes do banco de dados
db = create_engine("sqlite:///meubanco.db")

Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela para agrupar os usuarios
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

#Tabelas para agrupar os objetos
class Objeto(Base):
    __tablename__ = 'objetos'
    id = Column(Integer, primary_key=True)
    objeto = Column(String, primary_key=True)
    localidade = Column(String)
    data = Column(String)
    telefone= Column(String)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  # Chave estrangeira para o ID do usuário
    usuario = relationship("Usuario", backref="objetos_postados")  # Relacionamento com a tabela Usuario

    def __init__(self, objeto, localidade, data, telefone, user_id):
        self.objeto = objeto
        self.localidade = localidade
        self.data = data
        self.telefone= telefone
        self.user_id = user_id


Base.metadata.create_all(db)