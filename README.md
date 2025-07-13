<img width="597" height="278" alt="image" src="https://github.com/user-attachments/assets/73e5bb8d-95ed-4347-8ac5-108ca0c03baf" />



O projeto foi pensado com a ideia de solucionar um problema "simples", que até hoje não foi feito nenhuma medida realmente efetiva. A partir da "central de achados ufrpe", os estudantes e até mesmo funcionários, terão a oportunidade de ter acesso à uma plataforma em que poderão compartilhar objetos que a pessoa perdeu, ou que ela deseja encontrar. Facilitando assim, o alcance e a segurança na devolução do objeto a seu dono.


**BIBLIOTECAS USADAS:** 
### Importações do SQLAlchemy
Estas importações são responsáveis por:
- `create_engine`: Criar a conexão com o banco de dados
- `Column, Integer, String`: Definir os tipos de colunas do banco
- `text`: Permite executar consultas SQL puras
- : Gerenciar sessões do banco de dados `sessionmaker`
- : Criar a classe base para os modelos `declarative_base`
- `select`: Realizar consultas no banco

  ### Importação para Manipulação de Data/Hora
Esta importação é utilizada para:
- Validar o formato de datas inseridas no sistema
- Manipular informações temporais





### Principais Funcionalidades
#### 1. Gestão de Usuários
- **Criar usuário** (`create_user`):
    - Cadastra novos usuários
    - Valida se o email possui domínio @ufrpe.br
    - Verifica duplicidade de email

- **Login** (): `login_user`
    - Autenticação de usuários
    - Validação de credenciais

- **Atualização de senha** (): `atualizar_usuario`
    - Permite alteração de senha
    - Confirmação de nova senha

- **Busca de usuário** (): `buscar_usuario`
    - Consulta por email

- **Deletar usuário** (): `deletar_usuario`
    - Remove usuário do sistema

#### 2. Gestão de Objetos
- **Postagem** (`Blog` e `Postagem`):
    - Cadastro de objetos perdidos/encontrados
    - Registro de localização
    - Data do ocorrido
    - Contato do responsável

#### 3. Interface do Usuário
- **Menu Principal**:
    - Opções para gerenciamento de conta
    - Acesso ao sistema

- **Menu do Usuário** (`user_menu`):
    - Cadastro de novas postagens
    - Listagem de objetos
    - Opção de saída

### Características Técnicas
- Utiliza SQLAlchemy para ORM
- Banco de dados SQLite
- Validações de dados (ex: formato de data)
- Tratamento de exceções
- Sistema de sessões para gerenciamento de conexões

### Segurança e Validações
- Verificação de email institucional (@ufrpe.br)
- Confirmação de senha em alterações
- Validação de preenchimento obrigatório
- Verificação de formato de data


  ### Observações Importantes
- O sistema utiliza SQLite como banco de dados () `sqlite:///meubanco.db`
- Não há necessidade de bibliotecas adicionais além das mencionadas
- São utilizadas apenas bibliotecas padrão do Python e o SQLAlchemy

Para instalar as dependências necessárias, você pode usar o pip:
``` bash
pip install sqlalchemy
```
A biblioteca `datetime` já vem incluída na instalação padrão do Python.
      

  BIBLIOTECA DE FLUXOGRAMAS:
  https://drive.google.com/drive/folders/1hGhSBHsgDgNXkgziBX9Qe975HWyp7Lo2?usp=sharing
