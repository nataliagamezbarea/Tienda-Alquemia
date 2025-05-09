from flask import render_template, request, current_app
from routes.autentificacion.enviar_correo import enviar_correo

def contacto():
    return render_template('user/contacto/contacto.html')
