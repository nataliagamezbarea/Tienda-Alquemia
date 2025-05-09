from flask import render_template, session, redirect, url_for
from backend.Modelos.Usuario import Usuario

def informacion_personal():

    # Obtiene el user id 
    user_id = session.get("user")

    # Si no existe el user_id
    if not user_id:
        # Devuelve a la función para que inicie sesión
        return redirect(url_for("login"))

    # Filtra el usuario para obtener su información personal
    usuario = Usuario.query.filter_by(id_usuario=user_id).first()

     # Si el usuario no se existe
    if not usuario:
        # Devuelve usuario no encontrado
        return "Usuario no encontrado", 404

    # Le pasamos usuario y marcamos la pestaña activa
    return render_template('user/usuario_configuracion/informacion_personal.html',usuario=usuario)
