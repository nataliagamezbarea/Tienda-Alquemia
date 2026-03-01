from flask import render_template, request, redirect, session, url_for, flash
from backend.supabase_rest import select, _request

def pedido():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        pedido_id = request.form.get('pedido_id')
        nuevo_estado = (request.form.get('estado') or '').strip().lower()

        pedido_rows = select("pedidos", {"select": "id_pedido,estado", "id_pedido": f"eq.{pedido_id}", "limit": "1"})
        pedido_actual = pedido_rows[0] if pedido_rows else None

        if pedido_actual:
            if str(pedido_actual.get("estado", "")).lower() != nuevo_estado:
                _request("PATCH", "pedidos", params={"id_pedido": f"eq.{pedido_id}"}, payload={"estado": nuevo_estado})
                flash('El estado del pedido ha sido actualizado con éxito.', 'success')
            else:
                flash('El estado del pedido ya está actualizado.', 'info')
        else:
            flash('No se encontró el pedido.', 'error')

        return redirect(url_for('pedido'))  # Redirige para refrescar la página

    pedidos = select(
        "pedidos",
        {
            "select": "id_pedido,nombre_envio,apellido1_envio,apellido2_envio,estado,id_tienda",
            "order": "id_pedido.desc",
        },
    )

    tiendas = select("tiendas", {"select": "id_tienda,ciudad,pais"})
    tienda_map = {t.get("id_tienda"): t for t in tiendas}
    for p in pedidos:
        p["tienda"] = tienda_map.get(p.get("id_tienda"))

    return render_template('admin/pedidos/lista_pedidos.html', pedidos=pedidos)
