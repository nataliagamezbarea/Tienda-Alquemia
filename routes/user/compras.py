from flask import redirect, render_template, session, url_for
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from backend.Modelos import Pedido, PedidoProducto, ProductoVariante

def compras():
    # Obtiene el user_id
    user_id = session.get("user")

    # Si no existe el user_id
    if not user_id:
        # Devuelve a la función para logearte
        return redirect(url_for("login"))

    # Realiza una consulta con joinedload para obtener los productos relacionados
    pedidos = Pedido.query.options(
        joinedload(Pedido.pedido_productos)
        .joinedload(PedidoProducto.producto_variante)
        .joinedload(ProductoVariante.color),
        joinedload(Pedido.pedido_productos)
        .joinedload(PedidoProducto.producto_variante)
        .joinedload(ProductoVariante.talla),
        joinedload(Pedido.pedido_productos)
        .joinedload(PedidoProducto.producto_variante)
        .joinedload(ProductoVariante.producto)
    ).filter_by(id_usuario=user_id).all()  # Filtra por el id_usuario

    # Calcula las fechas de entrega y los días restantes
    for pedido in pedidos:
        fecha_pedido = pedido.fecha
        pedido.fecha_entrega_min = fecha_pedido + timedelta(days=3)
        pedido.fecha_entrega_max = fecha_pedido + timedelta(days=5)
        pedido.dias_restantes = (pedido.fecha_entrega_max - datetime.now().date()).days

    return render_template('user/usuario_configuracion/compras.html', pedidos=pedidos)
