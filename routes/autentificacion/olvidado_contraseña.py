
from flask import render_template, request, current_app
from backend.Modelos.Usuario import Usuario
from routes.autentificacion.enviar_correo import enviar_correo
from routes.autentificacion.tokens import obtener_clave_secreta

# Funcion de olvidado contraseña
def olvidado_contraseña():
   mensaje = None
   tipo_mensaje = None


    # Si el metodo es post
   if request.method == "POST":
       # Recolecta el email del formulario (con el atributo name)
       correo = request.form['email']

       # Guardar en una variable si el usuario ha sido encontrado
       usuario_encontrado = Usuario.query.filter_by(email=correo).first()

        # si ha sido encontrado
       if usuario_encontrado:
           # obtienes la clave secreta
           s = obtener_clave_secreta()
           
           # Convierte con el correo y el salto de la contraseña en un token de seguridad
           token = s.dumps(correo, salt='password-reset-salt')
           # Le das la url para poder recuperar la contraseña pero añade el token generado
           url_restablecer = f"http://localhost:5000/restablecer_contraseña/{token}"

            # Defines el mensaje del correo y le pasas la url
           cuerpo = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'


           # Llamamos a la función de correo pasando la instancia de la app
           enviar_correo(current_app, "Restablecimiento de Contraseña", correo, cuerpo)

           # Avisa que el correo ha sido enviado
           mensaje = "Correo enviado. Revisa tu bandeja de entrada."
           # Que ha tenido exito 
           tipo_mensaje = "exito"
       else:
           # Si no se encontro el usuario te salta un error
           mensaje = "No se encontró una cuenta asociada a ese correo."
           tipo_mensaje = "error"

   # Aqui pasas el mensaje y el tipo de mensjae
   return render_template('authentication/olvidado_contraseña.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)



