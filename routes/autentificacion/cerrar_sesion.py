from flask import redirect, url_for, session

def cerrar_sesion():

    # cambia
    session.pop("user", None)
    session.pop("is_admin", None)
    
    return redirect(url_for("login"))