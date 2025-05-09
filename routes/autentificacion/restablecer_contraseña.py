import bcrypt
from flask import render_template, request, redirect, url_for
from itsdangerous import SignatureExpired, BadSignature

from backend.Modelos.Usuario import Usuario
from backend.Modelos.database import db
from routes.autentificacion.tokens import obtener_clave_secreta

def restablecer_contraseña(token):
    # Obtener la instancia del serializador (con clave secreta interna)
    s = obtener_clave_secreta()

    try:
        # Decodificar el token para obtener el correo electrónico
        # El token es válido por 1 hora (3600 segundos)
        correo = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        # Si el token ha expirado, mostrar un mensaje de error
        return "El enlace ha expirado.", 400
    except BadSignature:
        # Si el token no es válido (modificado, mal formado, etc.), mostrar error
        return "El enlace no es válido.", 400

    # Si se envió el formulario (método POST)
    if request.method == "POST":
        # Obtener la nueva contraseña del formulario
        nueva_contraseña = request.form.get("nueva_contraseña")

        # Buscar al usuario por su correo
        usuario = Usuario.query.filter_by(email=correo).first()

        # Si el usuario existe y se ingresó una nueva contraseña
        if usuario and nueva_contraseña:
            # Encriptar la nueva contraseña con bcrypt
            hash_pw = bcrypt.hashpw(nueva_contraseña.encode("utf-8"), bcrypt.gensalt())

            # Guardar la contraseña encriptada en la base de datos
            usuario.contrasena = hash_pw.decode("utf-8")
            db.session.commit()

            # Redirigir al login tras restablecer la contraseña
            return redirect(url_for("login"))

    # Si es GET (o si algo falló), renderizar el formulario de restablecimiento
    return render_template("authentication/restablecer_contraseña.html", token=token)
