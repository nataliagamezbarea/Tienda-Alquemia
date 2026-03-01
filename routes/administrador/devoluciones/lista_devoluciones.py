from flask import render_template, redirect, url_for, session
from backend.supabase_rest import select


def lista_devoluciones():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devoluciones = select(
        "devoluciones",
        {
            "select": "id_devolucion,descripcion,id_pedido,id_variante,fecha_devolucion,hecha",
            "order": "id_devolucion.desc",
        },
    )
    rels = select("devoluciones_tiendas", {"select": "id_devolucion,id_tienda"})
    tiendas = select("tiendas", {"select": "id_tienda,pais,provincia,ciudad,codigo_postal,maps_url"})
    rel_map = {r.get("id_devolucion"): r.get("id_tienda") for r in rels}
    tienda_map = {t.get("id_tienda"): t for t in tiendas}

    devoluciones_con_tienda = []
    for devolucion in devoluciones:
        id_tienda = rel_map.get(devolucion.get("id_devolucion"))
        tienda_info = tienda_map.get(id_tienda) if id_tienda is not None else None

        devoluciones_con_tienda.append({
            'devolucion': devolucion,
            'tienda': tienda_info
        })

    return render_template(
        'admin/devoluciones/lista_devoluciones.html',
        devoluciones=devoluciones_con_tienda
    )
