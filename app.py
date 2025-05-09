import os
from dotenv import load_dotenv
from flask import Flask
from backend.Modelos.database import init_db
from flask_caching import Cache

from routes import *


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
app.add_url_rule('/busqueda','busqueda', busqueda, methods=["GET" , "POST"])

app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])



@app.context_processor
def inyectar_menu():
    menu_data = obtener_menu(cache)
    print(menu_data)  # Verifica los datos que se están obteniendo
    return dict(menu=obtener_menu(cache))



@app.context_processor
def inyectar_cesta():
    return dict(cesta=obtener_cesta())

# HOME
app.add_url_rule('/', 'home', home)

# AUTENTIFICACIÓN
app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
app.add_url_rule('/registro', 'registro', registro, methods=["GET", "POST"])
app.add_url_rule('/olvidado_contraseña', 'olvidado_contraseña', olvidado_contraseña, methods=["GET", "POST"])
app.add_url_rule('/restablecer_contraseña/<token>', 'restablecer_contraseña', restablecer_contraseña, methods=["GET", "POST"])

# USER
app.add_url_rule('/informacion_personal', 'informacion_personal', informacion_personal)
app.add_url_rule('/update_usuario', 'update_usuario', update_usuario, methods=['POST']) 
app.add_url_rule('/compras', 'compras', compras, methods=["GET", "POST"])
app.add_url_rule('/cerrar_sesion', 'cerrar_sesion', cerrar_sesion, methods=["GET", "POST"])
app.add_url_rule('/cambiar_contraseña', 'cambiar_contraseña', update_contraseña, methods=["GET", "POST"])


# TIENDA 
app.add_url_rule('/nosotros', 'nosotros', nosotros, methods=["GET"])
app.add_url_rule('/encuentranos', 'encuentranos', encuentranos, methods=["GET"])

# CONTACTANOS

app.add_url_rule('/contactanos', 'contactanos', contacto, methods=["GET"])
app.add_url_rule('/contactanos/particular', 'contactanos_particular', contacto_particular, methods=["GET", "POST"])
app.add_url_rule('/contactanos/empresa', 'contactanos_empresa', contacto_empresa, methods=["GET", "POST"])







if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
