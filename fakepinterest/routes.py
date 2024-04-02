# Criar as rotas do nosso site (LINKS)

# url_for PERMITE QUE VOCÊ PEGUE A URL DE ACORDO COM O NOME DA FUNÇÃO E NÃO DE ACORDO COM A ROTA
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user

from fakepinterest import app, database, bcrypt
from fakepinterest.forms import FormLogin, FormCriarConta
from fakepinterest.models import Usuario, Foto


# Definindo a rota do nosso site
@app.route('/', methods = ["GET", "POST"])
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        # BUSCANDO O USUÁRIO PELO EMAIL
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario:
            # VERIFICAR SE A SENHA DO USUÁRIO ESTÁ CORRETA
            # MAS ANTES DISSO TEMOS QUE DISCRIPTOGRAFAR A SENHA PARA COMPARAR COM A SENHA QUE FOI DIGITADA NO CAMPO DE LOGIN
            bcrypt.check_password_hash(usuario.senha, formlogin.senha.data)

            login_user(usuario, remember = True)
            return redirect(url_for("perfil", usuario = usuario.username))
        
    return render_template("homepage.html", form = formlogin)


@app.route("/criarconta", methods = ["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():

        # Criptografa a senha do usuário
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        # Criando uma instância do usuario
        usuario = Usuario(username = formcriarconta.username.data, email = formcriarconta.email.data, senha = senha)

        # salvando o usuário no banco
        database.session.add(usuario)
        database.session.commit()

        # após criar a conta essa função loga o usuário
        # remember = True LEMBRA QUE O USUÁRIO ESTÁ LOGADO SE ELE FECHAR A PÁGINA E VOLTAR
        login_user(usuario, remember = True)

        # redirecionando para a página de perfil
        return redirect(url_for("perfil", usuario = usuario.username))
    
    return render_template("criarconta.html", form = formcriarconta)


@app.route("/perfil/<usuario>") # <usuario> SIGNIFICA QUE A TAG USUÁRIO AGORA É UMA VARIÁVEL
@login_required # SIGNIFICA QUE ESSA FUNÇÃO SÓ PODERÁ SER ACESSADA SER O USUÁRIO ESTIVER LOGADO
def perfil(usuario: str):
    return render_template("perfil.html", usuario = usuario)
#                                                              <usuario> vai ser igual a o usuário que foi passado na função como parâmetro


@app.route("/logout")
@login_required
def logout():
    """Desloga o usuário e o redireciona  para a página de login
    """
    logout_user()
    return redirect(url_for("homepage"))
