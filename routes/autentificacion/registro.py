from flask import render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos.Usuario import Usuario
import bcrypt

def registro():
    if request.method == "POST":
        # Recoger datos del formulario
        nombre = request.form.get("nombre", "").strip()
        apellido1 = request.form.get("apellido1", "").strip()
        apellido2 = request.form.get("apellido2", "").strip()
        email = request.form.get("email", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar_contrasena = request.form.get("confirmar_contrasena", "")
        
        # Convertir el valor del radio a booleano
        cliente_tipo = request.form.get("cliente_tipo", "False") == "True"

        # Validar registro como empresa
        if cliente_tipo and not email.endswith("@tiendaalquemia.com"):
            return render_template(
                "authentication/registro.html",
                error="Solo los correos con dominio @tiendaalquemia.com pueden registrarse como empresa.",
                cliente_tipo=False
            )

        # Validar contraseñas
        if contrasena != confirmar_contrasena:
            return render_template(
                "authentication/registro.html",
                error="Las contraseñas no coinciden.",
                cliente_tipo=cliente_tipo
            )

        # Comprobar si el correo ya está registrado
        if Usuario.query.filter_by(email=email).first():
            return render_template(
                "authentication/registro.html",
                error="Correo electrónico ya registrado.",
                cliente_tipo=cliente_tipo
            )

        # Hashear la contraseña
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Crear el usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            email=email,
            contrasena=contrasena_encriptada,
            is_admin=cliente_tipo  # True si es empresa, False si es particular
        )

        # Guardar en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("login"))

    # GET request
    return render_template("authentication/registro.html", cliente_tipo=None)
