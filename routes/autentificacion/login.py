from flask import redirect, render_template, request, session, url_for
from backend.Modelos.Usuario import Usuario
import bcrypt

def login():
    # Si el usuarios ya ha iniciado sesión
    if "user" in session:
        if "is_admin" in session and session["is_admin"]:
            return render_template("admin/productos.html")
        return redirect(url_for('informacion_personal'))

    # Si es un POST (cuando se envían las credenciales)
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        usuario_encontrado = Usuario.query.filter_by(email=email).first()
        if usuario_encontrado and bcrypt.checkpw(contrasena.encode("utf-8"), usuario_encontrado.contrasena.encode("utf-8")):
            session["user"] = usuario_encontrado.id_usuario
            session["is_admin"] = usuario_encontrado.is_admin
            if usuario_encontrado.is_admin:
                return render_template("admin/productos.html")
            return redirect(url_for('informacion_personal'))
        else:
            error = "Email o contraseña incorrectos"
            return render_template("authentication/login.html", error=error)

    # Si no es POST, solo renderizas el formulario sin error
    return render_template("authentication/login.html")
