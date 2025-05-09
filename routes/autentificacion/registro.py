from flask import render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos.Usuario import Usuario
import bcrypt

def registro():
    # Si el método es post
    if request.method == "POST":

        # recopila los campos del formulario
        nombre = request.form["nombre"]
        apellido1 = request.form.get("apellido1", "")
        apellido2 = request.form.get("apellido2", "")
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]
        
       
        # Comprobar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            # pasar el tipo de cliente
            return render_template("authentication/registro.html", error="Las contraseñas no coinciden.", cliente_tipo=request.form.get('cliente_tipo'))
        
        # Verificar si el correo electrónico ya está registrado
        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            # devuelve un error 
            # se le sigue pasando el tipo para no olvidar la seleccion 
            return render_template("authentication/registro.html", error="Correo electrónico ya registrado.", cliente_tipo=request.form.get('cliente_tipo'))
        
        # recupera el cliente tipo  y si no se pasa nada va a ser false
        cliente_tipo = request.form.get("cliente_tipo", "False") 

        # ternaria si el cliente_tipo es true asigna al campo is_admin true y si no false
        is_admin = True if cliente_tipo == "True" else False  
        

        # hashea la constraseña y salt para que no se genere el mismo hash

        # NOTA : utf-8 funciona para convertir un string a bytes lo necesita para poder realizar hashing.
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Crear el nuevo usuario
        nuevo_usuario = Usuario( nombre=nombre, apellido1=apellido1, apellido2=apellido2,email=email,contrasena=contrasena_encriptada,is_admin=is_admin )

        # Añadirlo
        db.session.add(nuevo_usuario)

        # Guardar los cambios
        db.session.commit()

        # Si el usuario ya ha sido creado le llevamos para que se logee 
        return redirect(url_for("login"))

    # Cuando se haga get te va a llevar a registro
    return render_template("authentication/registro.html", cliente_tipo=None)
