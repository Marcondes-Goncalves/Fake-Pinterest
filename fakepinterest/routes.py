# Criar as rotas do nosso site (LINKS)

# url_for PERMITE QUE VOCÊ PEGUE A URL DE ACORDO COM O NOME DA FUNÇÃO E NÃO DE ACORDO COM A ROTA
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user

from fakepinterest import app, database, bcrypt
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto

import os
from werkzeug.utils import secure_filename

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
            return redirect(url_for("perfil", id_usuario = usuario.id))
        
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
        return redirect(url_for("perfil", id_usuario = usuario.id))
    
    return render_template("criarconta.html", form = formcriarconta)


@app.route("/perfil/<id_usuario>", methods = ["GET", "POST"]) # <usuario> SIGNIFICA QUE A TAG USUÁRIO AGORA É UMA VARIÁVEL
@login_required # SIGNIFICA QUE ESSA FUNÇÃO SÓ PODERÁ SER ACESSADA SER O USUÁRIO ESTIVER LOGADO
def perfil(id_usuario: int):
    if int(id_usuario) == current_user.id:# current_user pega o usuário que está logado
        # o usuário está vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            # Contém a foto 
            arquivo = form_foto.foto.data

            # tratando o nome do arquivo a função secure_filename
            nome_seguro = secure_filename(arquivo.filename)

            # salvar o arquivo na pasta fotos_posts
            # os.join(os.path.abspath(os.path.dirname(__file__)) está referênciando a raiz do caminho onde está o arquivo routes
            # app.config["UPLOAD_FOLDER"] contém o caminho onde as fotos dos usuários serão salvas
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"], nome_seguro)
            
            arquivo.save(caminho)

            # registrar o arquivo no banco de dados
            foto = Foto(imagem = nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario = current_user, form = form_foto)
    else:
        # ele está no perfil de outro usuário
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario = usuario, form = None)
#                                                              <usuario> vai ser igual a o usuário que foi passado na função como parâmetro


@app.route("/logout")
@login_required
def logout():
    """Desloga o usuário e o redireciona  para a página de login
    """
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos = fotos)

