
from flask import request, redirect, url_for, session

from backend.Modelos.database import db
from backend.Modelos.Cesta import Cesta
from backend.Modelos.CestaProducto import CestaProducto
from backend.Modelos.ProductoVariante import ProductoVariante

def añadir_producto_cesta():
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para añadir productos a la cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    id_producto = request.form.get('id_producto')
    id_color = request.form.get('id_color_radio')  # ← CORREGIDO aquí
    id_talla = request.form.get('id_talla')

    if not id_producto or not id_color or not id_talla:
        session['message'] = 'Faltan datos para añadir el producto.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    variante = ProductoVariante.query.filter_by(
        id_producto=id_producto,
        id_color=id_color,
        id_talla=id_talla
    ).first()

    if not variante:
        session['message'] = 'No se encontró la variante seleccionada.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    # Buscar o crear la cesta del usuario
    cesta = Cesta.query.filter_by(id_usuario=user_id).first()
    if not cesta:
        cesta = Cesta(id_usuario=user_id)
        db.session.add(cesta)
        db.session.commit()

    # Buscar si el producto ya está en la cesta
    producto_cesta = CestaProducto.query.filter_by(
        id_cesta=cesta.id_cesta,
        id_variante=variante.id_variante
    ).first()

    if producto_cesta:
        producto_cesta.cantidad += 1
    else:
        nuevo_producto_cesta = CestaProducto(
            id_cesta=cesta.id_cesta,
            id_variante=variante.id_variante,
            cantidad=1
        )
        db.session.add(nuevo_producto_cesta)

    db.session.commit()

    session['message'] = 'Producto añadido a tu cesta.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))
