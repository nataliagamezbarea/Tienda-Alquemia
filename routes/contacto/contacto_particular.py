
from flask import render_template, request, current_app
from routes.autentificacion.enviar_correo import enviar_correo



def contacto_particular():
    mensaje = None
    tipo_mensaje = None
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        email = request.form['email']
        telefono = request.form['telefono']
        tiquet = request.form['tiquet']
        comentario = request.form['comentario']
        opcion = request.form['opcion']  

        asunto = opcion 

        cuerpo = f"""
        Nombre: {nombre} {apellido1} {apellido2}
        Email: {email}
        Teléfono: {telefono}
        Nº tiquet/Pedido: {tiquet}
        Comentario: {comentario}
        """

        destino = "tiendaalquemiaparticular@gmail.com"

        # Enviar el correo
        enviar_correo(current_app, asunto, destino, cuerpo)

        # Mensaje de éxito
        mensaje = "El mensaje se ha enviado correctamente."
        tipo_mensaje = "exito"

        return render_template('user/contacto/contacto.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)

    return render_template('user/contacto/contacto.html')
