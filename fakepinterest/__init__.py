# Criação do App tem que ser feita em um arquivo com o nome __init__
from flask import Flask


app = Flask(__name__)


# As importações necessárias de outros módulos tem que ser feita após a criação ao App
from fakepinterest import routes
