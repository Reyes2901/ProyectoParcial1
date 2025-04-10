from flask import Flask
from admin import admin_bp  # Importar blueprint de admin
from client import client_bp  # Importar blueprint de cliente

app = Flask(__name__)
app.secret_key = 'secret_key'

# Registrar blueprint de admin y cliente
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(client_bp, url_prefix='/')

if __name__ == '__main__':
    # Cambiar el host a '0.0.0.0' para que sea accesible desde cualquier dirección IP en la red local
    app.run(debug=True, host='0.0.0.0', port=5000)
