from flask import request, redirect, url_for, session
from backend.supabase_rest import select, _request

def eliminar_producto_cesta(id_variante):
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para modificar tu cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    # Obtener la cesta del usuario
    cestas = select("cestas", {
        "select": "id_cesta,id_usuario",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    
    if not cestas:
        session['message'] = 'No tienes una cesta activa.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    id_cesta = cestas[0]["id_cesta"]

    # Buscar el producto en la cesta
    productos_cesta = select("cestas_productos", {
        "select": "id_cesta,id_variante,cantidad",
        "id_cesta": f"eq.{id_cesta}",
        "id_variante": f"eq.{id_variante}",
        "limit": "1"
    })

    if productos_cesta:
        _request("DELETE", "cestas_productos",
                params={"id_cesta": f"eq.{id_cesta}", "id_variante": f"eq.{id_variante}"})

    session['message'] = 'Producto eliminado de tu cesta.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))

def actualizar_cantidad_producto(id_variante):
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para modificar tu cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    nueva_cantidad = int(request.form.get('cantidad', 1))

    # Obtener la cesta del usuario
    cestas = select("cestas", {
        "select": "id_cesta,id_usuario",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    
    if not cestas:
        session['message'] = 'No tienes una cesta activa.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    id_cesta = cestas[0]["id_cesta"]

    # Buscar el producto en la cesta
    productos_cesta = select("cestas_productos", {
        "select": "id_cesta,id_variante,cantidad",
        "id_cesta": f"eq.{id_cesta}",
        "id_variante": f"eq.{id_variante}",
        "limit": "1"
    })

    if productos_cesta:
        if nueva_cantidad >= 1:
            _request("PATCH", "cestas_productos",
                    params={"id_cesta": f"eq.{id_cesta}", "id_variante": f"eq.{id_variante}"},
                    payload={"cantidad": nueva_cantidad})
        else:
            _request("DELETE", "cestas_productos",
                    params={"id_cesta": f"eq.{id_cesta}", "id_variante": f"eq.{id_variante}"})

    session['message'] = 'Cantidad actualizada correctamente.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))
