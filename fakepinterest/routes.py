# Criar as rotas do nosso site (LINKS)

# url_for PERMITE QUE VOCÊ PEGUE A URL DE ACORDO COM O NOME DA FUNÇÃO E NÃO DE ACORDO COM A ROTA
from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required


# Definindo a rota do nosso site
@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route("/perfil/<usuario>") # <usuario> SIGNIFICA QUE A TAG USUÁRIO AGORA É UMA VARIÁVEL
@login_required # SIGNIFICA QUE ESSA FUNÇÃO SÓ PODERÁ SER ACESSADA SER O USUÁRIO ESTIVER LOGADO
def perfil(usuario):
    return render_template("perfil.html", usuario = usuario)
#                                                              <usuario> vai ser igual a o usuário que foi passado na função como parâmetro
