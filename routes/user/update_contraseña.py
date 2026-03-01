from flask import request, redirect, url_for, session, render_template
import bcrypt
from backend.supabase_rest import select, _request

def update_contraseña():
    # Verificar si el usuario está logueado
    user_id = session.get("user")

    # Si el usuario no está logeado devuelve a la función login para poder logearse
    if not user_id:
        return redirect(url_for("login"))

    # Obtener el usuario desde Supabase
    usuarios = select("usuarios", {
        "select": "id_usuario,contrasena",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    usuario = usuarios[0] if usuarios else None

    if not usuario:
        return redirect(url_for("login"))

    mensaje = None
    tipo_mensaje = None

    # Si el método es post
    if request.method == "POST":
        # Obtener los valores del formulario
        actual = request.form.get("actual")
        nueva = request.form.get("nueva")
        confirmar = request.form.get("confirmar")

        # Verificar que la contraseña actual coincida con la almacenada en la base de datos
        if not bcrypt.checkpw(actual.encode('utf-8'), usuario["contrasena"].encode('utf-8')):
            mensaje = "La contraseña actual es incorrecta."
            tipo_mensaje = "error"
        # Verificar que las contraseñas nueva y confirmar coincidan
        elif nueva != confirmar:
            mensaje = "Las contraseñas no coinciden."
            tipo_mensaje = "error"
        else:
            # Encriptar la nueva contraseña y actualizarla en Supabase
            nueva_contrasena = bcrypt.hashpw(nueva.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            _request("PATCH", "usuarios",
                    params={"id_usuario": f"eq.{user_id}"},
                    payload={"contrasena": nueva_contrasena})
            mensaje = "Contraseña actualizada correctamente."
            tipo_mensaje = "exito"

    return render_template("user/usuario_configuracion/cambiar_contrasena.html", mensaje=mensaje,tipo_mensaje=tipo_mensaje)
