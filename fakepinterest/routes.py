# Criar as rotas do nosso site (LINKS)

# url_for PERMITE QUE VOCÊ PEGUE A URL DE ACORDO COM O NOME DA FUNÇÃO E NÃO DE ACORDO COM A ROTA
from flask import render_template
from flask_login import login_required

from fakepinterest import app
from fakepinterest.forms import FormLogin, FormCriarConta


# Definindo a rota do nosso site
@app.route('/', methods = ["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    return render_template("homepage.html", form = formlogin)


@app.route("/criarconta", methods = ["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    
    return render_template("criarconta.html", form = formcriarconta)


@app.route("/perfil/<usuario>") # <usuario> SIGNIFICA QUE A TAG USUÁRIO AGORA É UMA VARIÁVEL
@login_required # SIGNIFICA QUE ESSA FUNÇÃO SÓ PODERÁ SER ACESSADA SER O USUÁRIO ESTIVER LOGADO
def perfil(usuario):
    return render_template("perfil.html", usuario = usuario)
#                                                              <usuario> vai ser igual a o usuário que foi passado na função como parâmetro
