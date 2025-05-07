import os
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from backend.Modelos.database import init_db

from routes.home import home





# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Para el login
app.secret_key = os.urandom(24)  

# Configuración del correo utilizando variables de entorno
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Configuración de caché con Flask-Caching
app.config['CACHE_TYPE'] = 'simple'  # Puedes usar 'redis' o 'memcached' si es necesario
cache = Cache(app)

# Inicializar la base de datos
init_db(app)

app.add_url_rule('/', 'home', home)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
