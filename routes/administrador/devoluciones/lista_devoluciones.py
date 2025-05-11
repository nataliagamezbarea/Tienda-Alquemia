from flask import render_template, redirect, url_for, session
from backend.Modelos.Devoluciones_Tiendas import DevolucionesTiendas
from backend.Modelos.Devoluciones import Devoluciones


def lista_devoluciones():
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
