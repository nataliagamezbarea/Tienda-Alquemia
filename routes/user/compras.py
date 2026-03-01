from flask import redirect, render_template, session, url_for
from datetime import datetime, timedelta
from backend.supabase_rest import select

def compras():
    # Obtiene el user_id
    user_id = session.get("user")

    # Si no existe el user_id
    if not user_id:
        # Devuelve a la función para logearte
        return redirect(url_for("login"))

    # Obtiene los pedidos del usuario desde Supabase
    pedidos = select("pedidos", {
        "select": "id_pedido,id_usuario,fecha,estado",
        "id_usuario": f"eq.{user_id}"
    })

    # Para cada pedido, obtiene los productos asociados
    for pedido in pedidos:
        pedido_productos = select("pedidos_productos", {
            "select": "id_pedido_producto,id_pedido,id_producto_variante,cantidad,precio",
            "id_pedido": f"eq.{pedido['id_pedido']}"
        })
        
        # Para cada producto del pedido, obtiene información de la variante
        for pp in pedido_productos:
            variantes = select("productos_variantes", {
                "select": "id_producto_variante,id_producto,id_color,id_talla",
                "id_producto_variante": f"eq.{pp['id_producto_variante']}"
            })
            if variantes:
                pp["variante"] = variantes[0]
        
        pedido["pedido_productos"] = pedido_productos
        
        # Calcula las fechas de entrega y los días restantes
        fecha_pedido = datetime.strptime(pedido["fecha"], "%Y-%m-%d").date()
        pedido["fecha_entrega_min"] = fecha_pedido + timedelta(days=3)
        pedido["fecha_entrega_max"] = fecha_pedido + timedelta(days=5)
        pedido["dias_restantes"] = (pedido["fecha_entrega_max"] - datetime.now().date()).days

    return render_template('user/usuario_configuracion/compras.html', pedidos=pedidos)
