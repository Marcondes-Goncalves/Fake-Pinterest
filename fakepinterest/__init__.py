# Criação do App tem que ser feita em um arquivo com o nome __init__
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# AQUI DEFINIMOS QUAL BANCO IREMOS CRIAR
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

database = SQLAlchemy(app)


# As importações necessárias de outros módulos tem que ser feita após a criação ao App
from fakepinterest import routes
