from flask import Flask, render_template, url_for

# url_for PERMITE QUE VOCÊ PEGUE A URL DE ACORDO COM O NOME DA FUNÇÃO E NÃO DE ACORDO COM A ROTA

app = Flask(__name__)

# Definindo a rota do nosso site
@app.route('/')
def homepage():
    return render_template("homepage.html")

# <usuario> SIGNIFICA QUE A TAG USUÁRIO AGORA É UMA VARIÁVEL
@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario = usuario)
#                                                              <usuario> vai ser igual a o usuário que foi passado na função como parâmetro




if __name__ == "__main__":
    app.run(debug=True)
