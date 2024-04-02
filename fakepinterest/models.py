# Criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin # define a classe que vai gerênciar a estrutura de logins


# função para retornar o usuário pelo seu id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# database.Model: com esse parâmatro conseguiremos transformar a classe em uma tabela e uma tabela em uma classe.
class Usuario(database.Model, UserMixin):

    # primary_key = True O ID SERÁ INCREMENTADO AUTOMÁTICAMENTE A CADA NOVO USUÁRIO
    id: int = database.Column(database.Integer, primary_key = True)

    # nullable = False SIGNIFICA QUE ESSES CAMPOS NÃO PODEM SER NULLOS
    username: str = database.Column(database.String, nullable = False)
    senha: str = database.Column(database.String, nullable = False)

    # O usuário só proderá criar uma conta por email
    email: str = database.Column(database.String, nullable = False, unique = True)

    # fotos não vai ser uma  coluna, mas sim uma referência para classe Foto.
    fotos = database.relationship("Foto", backref = "usuario", lazy = True)


class Foto(database.Model):

    id: int = database.Column(database.Integer, primary_key = True)
    imagem = database.Column(database.String, default = "default.png")

    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.utcnow())

    # chave estrangeira que faz referência ao usuário   # type: ignore[Unknown]
    # note que a classe tem que ser passada em minusculas, pois no banco a mesma será criada com minusculas. 
    id_usuario: int = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable = False) 
