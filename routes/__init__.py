# HOME
from .home import home

# OBTENER MENU
from .obtener_menu import obtener_menu

# NAVBAR
from .busqueda import busqueda


# OBTENER_CESTA
from .obtener_cesta import obtener_cesta

# AUTENTIFICACIÓN
from .autentificacion.login import login
from .autentificacion.registro import registro
from .autentificacion.restablecer_contraseña import restablecer_contraseña
from .autentificacion.olvidado_contraseña import olvidado_contraseña



# USER
from .user.informacion_personal import informacion_personal
from routes.user.update_usuario import update_usuario
from routes.user.compras import compras
from .autentificacion.cerrar_sesion import cerrar_sesion


from .user.update_contraseña import update_contraseña


# NOSOTROS
from .nosotros import nosotros

# ENCUENTRANOS

from .encuentranos import encuentranos

# CONTACTO

from .contacto.contacto import contacto
from .contacto.contacto_empresa import contacto_empresa

from .contacto.contacto_particular import contacto_particular

# PRODUCTOS

from .productos.catalogo import catalogo
from .productos.producto_detalle import producto_detalle

# Cesta

from .cesta.añadir_producto_cesta import añadir_producto_cesta
from .cesta.actualizar_cantidad_producto import actualizar_cantidad_producto
from .cesta.eliminar_producto_cesta import eliminar_producto_cesta

# Productos

from .administrador.producto.añadir_producto import crear_producto
from .administrador.producto.actualizar_producto import actualizar_producto
from .administrador.producto.eliminar_producto import eliminar_producto
from .administrador.producto.leer_producto import obtener_productos_html

# Categorias


from .administrador.categoria.categorias import listar_categorias

from routes.administrador.categoria.crear_categoria import crear_categoria
from routes.administrador.categoria.categorias_editar import editar_categoria
from routes.administrador.categoria.categorias_eliminar import eliminar_categoria
from routes.administrador.pedido.pedido import pedido

# Devoluciones
from .administrador.devoluciones.crear_devolucion import crear_devolucion
from .administrador.devoluciones.editar_devolucion import editar_devolucion
from .administrador.devoluciones.eliminar_devolucion import eliminar_devolucion
from .administrador.devoluciones.editar_devolucion import editar_devolucion
from .administrador.devoluciones.obtener_devolucion import obtener_devolucion
from .administrador.devoluciones.lista_devoluciones import lista_devoluciones



# PAGAR

from routes.pedido.pagar import pagar
