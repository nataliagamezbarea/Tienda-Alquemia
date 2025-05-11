from flask import render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos.Usuario import Usuario
import bcrypt

def registro():
    if request.method == "POST":
        # Recoger datos del formulario
        nombre = request.form["nombre"]
        apellido1 = request.form.get("apellido1", "")
        apellido2 = request.form.get("apellido2", "")
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]
        cliente_tipo = request.form.get("cliente_tipo", "False")

        # Validar registro como empresa
        if cliente_tipo == "True" and not email.endswith("@tienda_alquemia.com"):
            return render_template(
                "authentication/registro.html",
                error="Solo los correos con dominio @tienda_alquemia.com pueden registrarse como empresa.",
                cliente_tipo="False"
            )

        # Validar contraseñas
        if contrasena != confirmar_contrasena:
            return render_template(
                "authentication/registro.html",
                error="Las contraseñas no coinciden.",
                cliente_tipo=cliente_tipo
            )

        # Comprobar si el correo ya está registrado
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template(
                "authentication/registro.html",
                error="Correo electrónico ya registrado.",
                cliente_tipo=cliente_tipo
            )

        # Determinar si es admin (empresa)
        is_admin = True if cliente_tipo == "True" else False

        # Hashear la contraseña
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Crear el usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            email=email,
            contrasena=contrasena_encriptada,
            is_admin=is_admin
        )

        # Guardar en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("authentication/registro.html", cliente_tipo=None)
