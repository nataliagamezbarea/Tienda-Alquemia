from flask import Flask, render_template, request, redirect, url_for, session
from backend.Modelos.Devoluciones_Tiendas import DevolucionesTiendas
from backend.Modelos.database import db
from backend.Modelos.Devoluciones import Devoluciones

def crear_devolucion_view():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        id_pedido = request.form['id_pedido']
        id_variante = request.form['id_variante']

        nueva_devolucion = Devoluciones(
            descripcion=descripcion,
            id_pedido=id_pedido,
            id_variante=id_variante,
            hecha=False
        )

        db.session.add(nueva_devolucion)
        db.session.commit()

        return redirect(url_for('lista_devoluciones'))

    return render_template('admin/devoluciones/crear_devolucion.html')

def lista_devoluciones_view():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devoluciones = Devoluciones.query.all()

    devoluciones_con_tienda = []
    for devolucion in devoluciones:
        relacion = DevolucionesTiendas.query.filter_by(id_devolucion=devolucion.id_devolucion).first()
        
        tienda_info = None
        if relacion and relacion.tienda:
            tienda = relacion.tienda
            tienda_info = {
                'id_tienda': tienda.id_tienda,
                'pais': tienda.pais,
                'provincia': tienda.provincia,
                'ciudad': tienda.ciudad,
                'codigo_postal': tienda.codigo_postal,
                'maps_url': tienda.maps_url
            }

        devoluciones_con_tienda.append({
            'devolucion': devolucion,
            'tienda': tienda_info
        })

    return render_template(
        'admin/devoluciones/lista_devoluciones.html',
        devoluciones=devoluciones_con_tienda
    )


def obtener_devolucion_view(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devolucion = Devoluciones.query.get(id_devolucion)
    if not devolucion:
        return "Devolución no encontrada", 404

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)


def editar_devolucion_view(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devolucion = Devoluciones.query.get(id_devolucion)
    if not devolucion:
        return "Devolución no encontrada", 404

    if request.method == 'POST':
        devolucion.descripcion = request.form['descripcion']
        devolucion.hecha = 'hecha' in request.form
        db.session.commit()
        return redirect(url_for('lista_devoluciones'))

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)


def eliminar_devolucion_view(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devolucion = Devoluciones.query.get(id_devolucion)
    if not devolucion:
        return "Devolución no encontrada", 404

    db.session.delete(devolucion)
    db.session.commit()
    return redirect(url_for('lista_devoluciones'))
