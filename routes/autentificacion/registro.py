from flask import render_template, request, redirect, url_for
from backend.supabase_rest import select, insert
import bcrypt

def registro():
    if request.method == "POST":
        # Recoger datos del formulario
        nombre = request.form.get("nombre", "").strip()
        apellido1 = request.form.get("apellido1", "").strip()
        apellido2 = request.form.get("apellido2", "").strip()
        email = request.form.get("email", "").strip().lower()
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

        # Cualquier correo corporativo de tiendaalquemia es administrador,
        # incluso si en el formulario se marcó "Particular".
        is_admin = cliente_tipo or email.endswith("@tiendaalquemia.com")

        # Validar contraseñas
        if contrasena != confirmar_contrasena:
            return render_template(
                "authentication/registro.html",
                error="Las contraseñas no coinciden.",
                cliente_tipo=cliente_tipo
            )

        # Comprobar si el correo ya está registrado
        existente = select("usuarios", {"select": "id_usuario", "email": f"eq.{email}", "limit": "1"})
        if existente:
            return render_template(
                "authentication/registro.html",
                error="Correo electrónico ya registrado.",
                cliente_tipo=cliente_tipo
            )

        # Hashear la contraseña
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        creado = insert(
            "usuarios",
            {
                "nombre": nombre,
                "apellido1": apellido1,
                "apellido2": apellido2 if apellido2 else None,
                "email": email,
                "contrasena": contrasena_encriptada,
                "is_admin": is_admin,
            },
        )

        if not creado:
            return render_template(
                "authentication/registro.html",
                error="No se pudo crear el usuario en Supabase.",
                cliente_tipo=cliente_tipo,
            )

        return redirect(url_for("login"))

    # GET request
    return render_template("authentication/registro.html", cliente_tipo=None)
