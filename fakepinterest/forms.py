# Criar os  formulários do nosso site

from flask_wtf import FlaskForm # Estrutura dos formulários
from wtforms import StringField, PasswordField, SubmitField # Campo de texto, de senha e botão de enviar
# Classe para validar os campos
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from fakepinterest.models import Usuario

class FormLogin(FlaskForm):

    email:str = StringField("E-mail", validators = [DataRequired(), Email()])
    senha: str = PasswordField("Senha", validators = [DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")


class  FormCriarConta(FlaskForm):

    email: str = StringField("E-mail", validators = [DataRequired(), Email()])
    username: str = StringField("Nome de usuário", validators = [DataRequired()])

    # Length(6, 20): A senha tem que ter entre 6 e 20 caracteres ou números.
    senha:str = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    confirmacao_senha: str = PasswordField("Confirmação de Senha", validators = [DataRequired(), EqualTo("senha")])

    botao_confirmacao = SubmitField("Criar Conta")
    

    # Quando criar funções de validação temos que passar validate (_NOME DO CAMPO QUE VAI SER VALIDADO)
    def validate_email(self, email: str):
        """Função para verificar se o E-mail digitado já foi cadastrado.
        email: str | atributo email do FormCriarConta
        Return: Se o email já estiver cadastrado retorna um erro pedindo para o usuário logar na conta.
        """
        # email.data SIGNIFICA QUE ESTAMOS PEGANDO A INFORMAÇÃO QUE FOI PREENCHIDA NO CAMPO DE EMAIL
        usuario = Usuario.query.filter_by(email = email.data).first() 
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")
