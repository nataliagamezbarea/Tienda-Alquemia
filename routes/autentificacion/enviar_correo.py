from flask_mail import Mail, Message

# Instancia de Flask-Mail global
mail = Mail()

def enviar_correo(app, asunto, destinatario, cuerpo, archivos=None):

    mail.init_app(app)

    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo

    # Si hay archivos, los adjuntamos
    if archivos:
        for archivo in archivos:
            with app.open_resource(archivo) as adjunto:
                filename = archivo.split("/")[-1]  # Nombre del archivo
                msg.attach(filename, "application/octet-stream", adjunto.read())

    mail.send(msg)
