#Importações necessarias
#Usando sqlalchemy como banco de dados
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base
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
    objeto = Column(String, primary_key=True)
    localidade = Column(String)
    data = Column(String)
    telefone= Column(String)

    def __init__(self, objeto, localidade, data, telefone):
        self.objeto = objeto
        self.localidade = localidade
        self.data = data
        self.telefone= telefone

Base.metadata.create_all(db)
#------------------------------------------------------------------------
#Criar usuário
def create_user():
    nome = input("Digite seu nome: ")
    email = input("Digite seu email(@ufrpe.br): ")
    senha = input("Digite sua senha: ")

    verify_user= get_user_by_email(session, email)
#verifica se o dominio da rural ta no email
    if "@ufrpe.br" not in email:
        print("email invalido"  )
        return
#verifica se o email ja esta cadastrado no banco
    if verify_user: 
        print("Email já cadastrado, tente a opção de login")
#salva no banco
    else:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        # Salvar no banco
        session.add(novo_usuario)
        session.commit()
        print("Usuário salvo com sucesso!")
        user_menu()

#Buscar o usuario pelo email
def get_user_by_email(session, email: str):
    #Retorna o usuário caso ele já esteja cadastrado ou None
    usuario = session.query(Usuario).filter_by(email=email).first()
    return usuario


#Login

def login_user(email, senha):
    session = Session()
    #verifica os dados do usuario
    user = session.query(Usuario).filter_by(email=email).first()
#caso nao seja encontrado o usuario no banco
    if not user:
        print("Usuário não encontrado")
        return False
    if user.senha == senha:
        print(f'Bem vindo, {user.nome}')
        return True
    else:
        print("Senha incorreta")
        return False


#Buscar usuário pelo email, para verificar se um usuario ja se encontra cadastrado
def buscar_usuario():
    email_busca = input("Digite o email do usuário que deseja buscar: ")
    usuario = session.query(Usuario).filter_by(email=email_busca).first()

    if usuario:
        print(f"Usuário encontrado: {usuario.nome} (E-mail: {usuario.email})")
    else:
        print("Usuário não encontrado.")


#UPDATE, atualizar a senha do usuario
def atualizar_usuario(usuario):
    nova_senha= input("Digite a nova senha:")
    confirma_nova_senha = input("Digite novamente a nova senha:")
    if nova_senha == confirma_nova_senha:
        try:
            usuario.senha = nova_senha 
            session.add(usuario)
            session.commit()
            print(f"Usuário '{usuario.nome}' atualizado com sucesso.")
        # Trata possíveis erros na atualização
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar usuário: {e}")
        finally:
            session.close()
    else:
        print("Erro ao atualizar senha. Tente novamente")


#DELETAR, apagar o usuario do database
def deletar_usuario(nome_usuario):
    session = Session()
    try:
        usuario = session.query(Usuario).filter_by(email=nome_usuario).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            print(f"Usuário '{nome_usuario}' deletado com sucesso.")
        # Trata possíveis erros na remoção
        else:
            print(f"Usuário '{nome_usuario}' não encontrado.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar usuário: {e}")


#OBJETO-EM DESENVOLVIMENTO
    ###Valida o formato da data###
def validar_data(data: str) -> None:

        try:
             datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            return 0



#Gerenciar os objetos
class Postagem:
    def __init__(self,objeto:str, localidade:str,data:str, telefone:int ):
        self.objeto= objeto
        self.localidade = localidade

        self.data= data
        self.telefone= telefone




    def __repr__(self):
        return f"Postagem(Objeto='{self.objeto}', localidade='{self.localidade}', data='{self.data}, telefone para contato='{self.telefone})"
#Gerenciar as postagens
class Blog:
    def __init__(self):
        self.postagens = [] #Armazena os objetos
#Adicionar postagens
    def adicionar_postagem(self, objeto, localidade, data, telefone):
        if not all([objeto, localidade, data, telefone]): #verifica se todos os dados foram preenchidos
            raise ValueError("Todos os campos devem ser preenchidos.")



        nova_postagem = Objeto(objeto=objeto, localidade=localidade, data=data, telefone=telefone)
        # Salvar no banco
        session.add(nova_postagem)
        session.commit()



#Lista de postagens cadastradas
    def listar_postagens(self):
        objetos = session.query(Objeto).all()

        if not objetos:
            print("Objeto não cadastrado")
        else:
            # Liste os objetos
            for obj in objetos:
                print(f"Objeto: {obj.objeto}, Localidade: {obj.localidade}, Data: {obj.data}, Telefone: {obj.telefone}")

def main():
    session = Session()



#"interface" do usuario apos o login/cadastrado
def user_menu():
    blog = Blog()
    while True:
        print("Bem-vindo ao sistema de achados e perdidos")
        print("1. Cadastrar nova postagem")
        print("2. Listar postagens")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Digite o nome e a descrição do objeto: ")
            conteudo = input("Digite onde foi encontrado/perdido: ")
            data = input("Digite a data que foi achado/perdido: ")
            validar=validar_data(data)
            if validar==0:
                print(f'Formato de data incorrteto(dd/mm/aaaa)')
                user_menu()
            telefone= input("Digite o número para contato: ")
            try:
                blog.adicionar_postagem(titulo, conteudo, data,telefone)
                print("Postagem cadastrada com sucesso")
            except ValueError as e:
                print(f"Erro ao cadastrar: {e}")


        elif opcao == '2':
            blog.listar_postagens()

        elif opcao == '3':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")



parar = False
#MENU incial
while not parar:
    print("******************************INICIO*********************************")
    print("Escolha uma opção:")
    print("1 - Criar usuário")
    print("2 - Buscar usuário")
    print("3 - Deletar usuário")
    print("4- Login")
    print("5- Sair")
    print("6-Atulizar senha")

    opcao = input("Digite sua opção: ")

    if opcao == '1':
        create_user()
    elif opcao == '2':
        buscar_usuario()
    elif opcao == '3':
       nome= input("Digite o email de usuário a ser deletado:")
       deletar_usuario(nome)
    elif opcao == '4':
        user= input("Digite seu email:")
        senha= input("Digite sua senha:")
        logou = login_user(user,senha)
        if logou:
            print("Login realizado com sucesso!")
            user_menu()
        else:
            print("Login falhou. Tente novamente.")
    elif opcao == '5':
        parar = True
    elif opcao=="6":
       email_cadastrado= input("Digite seu email cadastrado: ")
       usuario = session.query(Usuario).filter_by(email=email_cadastrado).first()
       if usuario:
          atualizar_usuario(usuario)
       else:
           print("Usuário não encontrado")
    else:
        print("Opção inválida. Tente novamente.")






if __name__ == "__main__":
    main()





#´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
