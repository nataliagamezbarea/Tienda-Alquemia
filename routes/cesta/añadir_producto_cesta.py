from flask import request, redirect, url_for, session
from backend.supabase_rest import select, insert, _request

def añadir_producto_cesta():
    user_id = session.get("user")
    if not user_id:
        session['message'] = 'Debes iniciar sesión para añadir productos a la cesta.'
        session['message_type'] = 'error'
        return redirect(url_for('login'))

    id_producto = request.form.get('id_producto')
    id_color = request.form.get('id_color_radio')
    id_talla = request.form.get('id_talla')

    if (
        not id_producto or not id_color or not id_talla
        or id_producto == "None" or id_color == "None" or id_talla == "None"
    ):
        session['message'] = 'Faltan datos para añadir el producto.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    # Verificar que la variante existe
    variantes = select("productos_variantes", {
        "select": "id_variante,id_producto,id_color,id_talla",
        "id_producto": f"eq.{id_producto}",
        "id_color": f"eq.{id_color}",
        "id_talla": f"eq.{id_talla}",
        "limit": "1"
    })
    
    if not variantes:
        session['message'] = 'No se encontró la variante seleccionada.'
        session['message_type'] = 'error'
        return redirect(request.referrer or url_for('home'))

    id_variante = variantes[0]["id_variante"]

    # Buscar o crear la cesta del usuario
    cestas = select("cestas", {
        "select": "id_cesta,id_usuario",
        "id_usuario": f"eq.{user_id}",
        "limit": "1"
    })
    
    if cestas:
        id_cesta = cestas[0]["id_cesta"]
    else:
        nueva_cesta = insert("cestas", {"id_usuario": user_id})
        id_cesta = nueva_cesta[0]["id_cesta"] if nueva_cesta else None
        if not id_cesta:
            session['message'] = 'Error al crear la cesta.'
            session['message_type'] = 'error'
            return redirect(request.referrer or url_for('home'))

    # Buscar si el producto ya está en la cesta
    productos_cesta = select("cestas_productos", {
        "select": "id_cesta,id_variante,cantidad",
        "id_cesta": f"eq.{id_cesta}",
        "id_variante": f"eq.{id_variante}",
        "limit": "1"
    })

    if productos_cesta:
        producto_cesta = productos_cesta[0]
        nueva_cantidad = producto_cesta["cantidad"] + 1
        _request("PATCH", "cestas_productos",
                params={"id_cesta": f"eq.{id_cesta}", "id_variante": f"eq.{id_variante}"},
                payload={"cantidad": nueva_cantidad})
    else:
        insert("cestas_productos", {
            "id_cesta": id_cesta,
            "id_variante": id_variante,
            "cantidad": 1
        })

    session['message'] = 'Producto añadido a tu cesta.'
    session['message_type'] = 'success'
    return redirect(request.referrer or url_for('home'))
