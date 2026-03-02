
import os
from flask import render_template, request, current_app
from backend.supabase_rest import select
from routes.autentificacion.enviar_correo import enviar_correo
from routes.autentificacion.tokens import obtener_clave_secreta

# Funcion de olvidado contraseña
def olvidado_contrasena():
    mensaje = None
    tipo_mensaje = None

    # Si el metodo es post
    if request.method == "POST":
        # Recolecta el email del formulario (con el atributo name)
        correo = request.form['email'].strip().lower()

        # Guardar en una variable si el usuario ha sido encontrado
        usuarios = select("usuarios", {"select": "id_usuario,email", "email": f"eq.{correo}", "limit": "1"})
        usuario_encontrado = usuarios[0] if usuarios else None

        # si ha sido encontrado
        if usuario_encontrado:
            # obtienes la clave secreta
            s = obtener_clave_secreta()

            # Convierte con el correo y el salto de la contraseña en un token de seguridad
            token = s.dumps(correo, salt='password-reset-salt')
            # Le das la url para poder recuperar la contraseña pero añade el token generado
            app_url = os.getenv('APP_URL', 'http://localhost:5000')
            url_restablecer = f"{app_url}/restablecer_contrasena/{token}"

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
    return render_template('authentication/olvidado_contrasena.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)



