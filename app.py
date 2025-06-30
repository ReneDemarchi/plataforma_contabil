from flask import Flask
from routes.login import auth
from routes.perfil import perfil
from routes.cliente import cliente


app = Flask(__name__)
app.secret_key = 'chave_secreta'

app.register_blueprint(auth)
app.register_blueprint(perfil)
app.register_blueprint(cliente)

if __name__ == '__main__':
    app.run(debug=True)
