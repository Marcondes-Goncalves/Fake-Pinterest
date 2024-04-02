# Criação do App tem que ser feita em um arquivo com o nome __init__
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# AQUI DEFINIMOS QUAL BANCO IREMOS CRIAR
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# essa senha foi gerada com o código: print(secrets.token_hex(16))
app.config["SECRET_KEY"] = "87840091186a87e7eb31b27fca616ab0" 
# definindo onde será feito os uploads das imagens do usuário
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
# CRIPTOGRAFA AS SENHAS
bcrypt = Bcrypt(app)
# GERÊNCIA O LOGIN
login_manager = LoginManager(app) 

# pra onde o usuário será redirecionado caso não esteja mais logado.
login_manager.login_view = "homepage"

# As importações necessárias de outros módulos tem que ser feita após a criação ao App
from fakepinterest import routes
