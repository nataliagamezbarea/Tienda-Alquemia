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



@app.context_processor
def inyectar_menu():
    menu_data = obtener_menu(cache)
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

# Productos

app.add_url_rule('/catalogo', 'catalogo', catalogo, methods=["GET"])
app.add_url_rule('/producto/<int:id_producto>', 'producto_detalle', producto_detalle, methods=["GET"])


app.add_url_rule('/producto/<int:id_producto>', 'producto_detalle', producto_detalle, methods=["GET"])


#  Cesta

app.add_url_rule('/cesta/añadir', 'añadir_producto_cesta', añadir_producto_cesta, methods=["POST"])
app.add_url_rule('/cesta/actualizar/<int:id_variante>', 'actualizar_cantidad_producto', actualizar_cantidad_producto, methods=["POST"])
app.add_url_rule('/cesta/eliminar/<int:id_variante>', 'eliminar_producto_cesta', eliminar_producto_cesta, methods=["POST"])



# Productos
app.add_url_rule('/productos', 'productos', obtener_productos_html, methods=['GET'])

# Ruta para mostrar el formulario de creación de un producto (GET) y procesar el formulario (POST)
app.add_url_rule('/producto/nuevo', 'crear_producto', crear_producto, methods=['GET', 'POST'])

# Ruta para mostrar el formulario de actualización de un producto (GET) y procesar la actualización (POST)
app.add_url_rule('/producto/editar/<int:producto_id>', 'actualizar_producto', actualizar_producto, methods=['GET', 'POST'])

# Ruta para eliminar un producto (solo POST)
app.add_url_rule('/producto/eliminar/<int:id_producto>', 'eliminar_producto', eliminar_producto, methods=['POST'])


# Categorias

app.add_url_rule('/categorias', 'listar_categorias', listar_categorias, methods=['GET'])
app.add_url_rule('/categorias/crear', 'crear_categoria', crear_categoria, methods=['GET', 'POST'])

app.add_url_rule('/categorias/editar/<int:categoria_id>', 'editar_categoria', editar_categoria, methods=['GET', 'POST'])
app.add_url_rule('/categorias/eliminar/<int:categoria_id>', 'eliminar_categoria', eliminar_categoria, methods=['POST'])

# Devoluciones

app.add_url_rule('/devoluciones', 'lista_devoluciones', lista_devoluciones, methods=['GET'])
app.add_url_rule('/devoluciones/nueva', 'nueva_devolucion', crear_devolucion, methods=['GET', 'POST'])
app.add_url_rule('/devoluciones/<int:id_devolucion>', 'obtener_devolucion', obtener_devolucion, methods=['GET'])
app.add_url_rule('/devoluciones/editar/<int:id_devolucion>', 'editar_devolucion', editar_devolucion, methods=['GET', 'POST'])
app.add_url_rule('/devoluciones/eliminar/<int:id_devolucion>', 'eliminar_devolucion', eliminar_devolucion, methods=['POST'])


# Pedido

app.add_url_rule("/pagar" , 'pagar' , pagar )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
