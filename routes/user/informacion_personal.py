from flask import render_template, session, redirect, url_for
from backend.supabase_rest import select

def informacion_personal():

    # Obtiene el user id 
    user_id = session.get("user")

    # Si no existe el user_id
    if not user_id:
        # Devuelve a la función para que inicie sesión
        return redirect(url_for("login"))

    # Filtra el usuario para obtener su información personal desde Supabase
    usuarios = select("usuarios", {
        "select": "id_usuario,nombre,apellido1,apellido2,email,is_admin",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    usuario = usuarios[0] if usuarios else None

    # Si el usuario no se existe
    if not usuario:
        # Devuelve usuario no encontrado
        return "Usuario no encontrado", 404

    # Le pasamos usuario y marcamos la pestaña activa
    return render_template('user/usuario_configuracion/informacion_personal.html',usuario=usuario)
