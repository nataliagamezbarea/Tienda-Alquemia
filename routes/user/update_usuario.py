from flask import request, redirect, url_for, session, render_template
from backend.supabase_rest import select, _request

def update_usuario():
    # Obtiene el usuario id
    user_id = session.get("user")

    # Si  no se ha logeado lleva a la función del login para que se pueda logear
    if not user_id:
        return redirect(url_for("login"))

    # Verificar que el usuario existe
    usuarios = select("usuarios", {
        "select": "id_usuario",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    usuario = usuarios[0] if usuarios else None

    # Si no se encuentra el usuario
    if not usuario:
        return "Usuario no encontrado", 404

    # Obtener datos del formulario
    nombre = request.form.get("nombre")
    apellido1 = request.form.get("apellido1")
    apellido2 = request.form.get("apellido2")
    email = request.form.get("email")

    # Actualizar los campos en Supabase
    payload = {
        "nombre": nombre,
        "apellido1": apellido1,
        "apellido2": apellido2,
        "email": email
    }
    
    _request("PATCH", "usuarios", 
             params={"id_usuario": f"eq.{user_id}"},
             payload=payload)

    # Redirigir a la página de información personal con los datos actualizados
    return redirect(url_for("informacion_personal"))
