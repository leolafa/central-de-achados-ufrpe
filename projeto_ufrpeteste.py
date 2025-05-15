from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select


db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabelas
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


class Objeto(Base):
    __tablename__ = 'objetos'
    objeto = Column(String, primary_key=True)
    localidade = Column(Integer)
    data = Column(Integer)

    def __init__(self, objeto, localidade, data):
        self.objeto = objeto
        self.localidade = localidade
        self.data = data

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
        print("email invalido")
        return
    if verify_user: 
        print("Email já cadastrado, tente a opção de login")
    else:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        # Salvar no banco
        session.add(novo_usuario)
        session.commit()
        print("Usuário salvo com sucesso!")


def get_user_by_email(session, email: str):
    #Retorna o usuário caso ele já esteja cadastrado ou None
    usuario = session.query(Usuario).filter_by(email=email).first()
    return usuario


#Login 
def login_user(email, senha):
    session = Session()
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
            print(f"Usuário '{nome_usuario}' atualizado com sucesso.")
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
        usuario = session.query(Usuario).filter_by(nome=nome_usuario).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            print(f"Usuário '{nome_usuario}' deletado com sucesso.")
        else:
            print(f"Usuário '{nome_usuario}' não encontrado.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar usuário: {e}")


#OBJETO-EM DESENVOLVIMENTO
class Postagem:
    def __init__(objeto, localidade,data):
        self.objeto= objeto
        self.localidade = localidade
        self.data= data

    def __repr__(self):
        return f"Postagem(Objeto={self.objeto}, conteudo={self.localididade}, data={self.data})"

class Blog:
    def __init__(self):
        self.postagens = []

    def adicionar_postagem(self, objeto, localidade, data):
        nova_postagem = Postagem(objeto, localidade, data)
        self.postagens.append(nova_postagem)

    def listar_postagem(self):
        if not self.postagens:
            print("Objeto não cadastrado")
        else:
            print("Objeto cadastrado:")
            for postagem in self.postagens:
                print(f"Objeto:{postagem.objeto} - {postagem.conteudo}- {postagem.data}")

def main():
    session = Session()

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
       nome= input("Digite o usuário a ser deletado:")
       deletar_usuario(nome)
    elif opcao == '4':
        user= input("Digite seu email:")
        senha= input("Digite sua senha:")
        login_user(user,senha)
    elif opcao == '5':
        parar = True
    elif opcao=="6":
       nome_usuario= input("Digite seu nome de usuário: ")
       usuario = session.query(Usuario).filter_by(nome=nome_usuario).first()
       if usuario:
          atualizar_usuario(usuario)
       else:
           print("Usuário não encontrado")
    else:
        print("Opção inválida. Tente novamente.")



#Parte da postagem de objeto- EM DESENVOLVIMENTO
    #while True:
        print("Bem-vindo ao sistema de achados e perdidos")
        print("1. Cadastrar nova postagem")
        print("2. Listar postagens")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Digite o nome e a descrição do objeto: ")
            conteudo = input("Digite onde foi encontrado: ")
            data = input("Digite a data que foi achado: ")
            Blog.adicionar_postagem(titulo, conteudo, data)
            print("Postagem cadastrada com sucesso!")

        elif opcao == '2':
            Blog.listar_postagens()

        elif opcao == '3':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()





#´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´
