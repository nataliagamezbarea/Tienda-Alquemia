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
