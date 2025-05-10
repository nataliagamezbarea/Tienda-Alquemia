
from flask import request, redirect, url_for, session

from backend.Modelos.database import db
from backend.Modelos.Cesta import Cesta
from backend.Modelos.CestaProducto import CestaProducto
from backend.Modelos.ProductoVariante import ProductoVariante

def actualizar_cantidad_producto(id_variante):
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para modificar tu cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    nueva_cantidad = int(request.form.get('cantidad', 1))

    cesta = Cesta.query.filter_by(id_usuario=user_id).first()
    if not cesta:
        session['message'] = 'No tienes una cesta activa.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    producto_cesta = CestaProducto.query.filter_by(
        id_cesta=cesta.id_cesta,
        id_variante=id_variante
    ).first()

    if producto_cesta:
        if nueva_cantidad >= 1:
            producto_cesta.cantidad = nueva_cantidad
            db.session.commit()
        else:
            # Si la cantidad es menor que 1, elimina el producto
            db.session.delete(producto_cesta)
            db.session.commit()

    session['message'] = 'Cantidad actualizada correctamente.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))
