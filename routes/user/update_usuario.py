from flask import request, redirect, url_for, session, render_template
from backend.Modelos.Usuario import Usuario
from backend.Modelos.database import db  

def update_usuario():
    # Obtiene el usuario id
    user_id = session.get("user")

    # Si  no se ha logeado lleva a la función del login para que se pueda logear
    if not user_id:
        return redirect(url_for("login"))

    # Filtra el usuario por el id del que se ha logeadp
    usuario = Usuario.query.filter_by(id_usuario=user_id).first()

    # Si no se encuentra el usuario
    if not usuario:
        return "Usuario no encontrado", 404

    # Obtener datos del formulario
    nombre = request.form.get("nombre")
    apellido1 = request.form.get("apellido1")
    apellido2 = request.form.get("apellido2")
    email = request.form.get("email")

    # Actualizar los campos
    usuario.nombre = nombre
    usuario.apellido1 = apellido1
    usuario.apellido2 = apellido2
    usuario.email = email

    # Guardar cambios en la base de datos
    db.session.commit()

    # Redirigir a la página de información personal con los datos actualizados
    return redirect(url_for("informacion_personal"))
