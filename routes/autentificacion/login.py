from flask import redirect, render_template, request, session, url_for
from backend.supabase_rest import select, _request
import os
import bcrypt

def login():
    # Si el usuarios ya ha iniciado sesión
    if "user" in session:
        if "is_admin" in session and session["is_admin"]:
            return redirect(url_for("productos"))
        return redirect(url_for('informacion_personal'))

    # Si es un POST (cuando se envían las credenciales)
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        contrasena = request.form["contrasena"]
        admin_domain = os.getenv("ADMIN_EMAIL_DOMAIN", "tiendaalquemia.com").lower().lstrip("@")

        usuarios = select("usuarios", {"select": "id_usuario,email,contrasena,is_admin", "email": f"eq.{email}", "limit": "1"})
        usuario_encontrado = usuarios[0] if usuarios else None

        if usuario_encontrado and bcrypt.checkpw(contrasena.encode("utf-8"), str(usuario_encontrado.get("contrasena", "")).encode("utf-8")):
            email_usuario = str(usuario_encontrado.get("email", "")).lower()
            es_admin = bool(usuario_encontrado.get("is_admin")) or email_usuario.endswith(f"@{admin_domain}")

            # Corrige usuarios ya existentes que se registraron como particular
            if es_admin and not bool(usuario_encontrado.get("is_admin")):
                _request(
                    "PATCH",
                    "usuarios",
                    params={"id_usuario": f"eq.{usuario_encontrado.get('id_usuario')}"},
                    payload={"is_admin": True},
                )

            session["user"] = usuario_encontrado.get("id_usuario")
            session["is_admin"] = es_admin
            if session["is_admin"]:
                return redirect(url_for('productos'))
            return redirect(url_for('informacion_personal'))
        else:
            error = "Email o contraseña incorrectos"
            return render_template("authentication/login.html", error=error)

    # Si no es POST, solo renderizas el formulario sin error
    return render_template("authentication/login.html")
