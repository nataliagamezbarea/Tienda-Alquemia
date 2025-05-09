from flask import request, redirect, url_for, session, render_template
import bcrypt
from backend.Modelos.Usuario import Usuario
from backend.Modelos.database import db

def update_contraseña():
    # Verificar si el usuario está logueado
    user_id = session.get("user")

    # Si el usuario no está logeado devuelve a la función login para poder logearse
    if not user_id:
        return redirect(url_for("login"))

    # Obtener el usuario desde la base de datos
    usuario = Usuario.query.filter_by(id_usuario=user_id).first()

    mensaje = None
    tipo_mensaje = None

    # Si el método es post
    if request.method == "POST":
        # Obtener los valores del formulario
        actual = request.form.get("actual")
        nueva = request.form.get("nueva")
        confirmar = request.form.get("confirmar")

        # Verificar que la contraseña actual coincida con la almacenada en la base de datos
        if not bcrypt.checkpw(actual.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            mensaje = "La contraseña actual es incorrecta."
            tipo_mensaje = "error"
        # Verificar que las contraseñas nueva y confirmar coincidan
        elif nueva != confirmar:
            mensaje = "Las contraseñas no coinciden."
            tipo_mensaje = "error"
        else:
            # Encriptar la nueva contraseña y actualizarla
            usuario.contrasena = bcrypt.hashpw(nueva.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Inserta los cambios a la base de datos
            db.session.commit()
            mensaje = "Contraseña actualizada correctamente."
            tipo_mensaje = "exito"

    return render_template("user/usuario_configuracion/cambiar_contraseña.html", mensaje=mensaje,tipo_mensaje=tipo_mensaje)
