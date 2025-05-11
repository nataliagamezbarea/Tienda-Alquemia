from flask import render_template, redirect, url_for, session
from backend.Modelos import Usuario
from backend.Modelos.database import db
from backend.Modelos.Pedido import Pedido
from backend.Modelos.PedidoProducto import PedidoProducto
from backend.Modelos.Cesta import Cesta
from backend.Modelos.CestaProducto import CestaProducto
from backend.Vistas.VistaProductoCompleto import VistaProductoCompleto
from datetime import datetime
from decimal import Decimal
from routes.obtener_cesta import obtener_cesta

def pedido_exitoso():
    if "user" not in session or not session.get("user"):
        return redirect(url_for('login'))

    id_usuario = session["user"]
    datos_cesta = obtener_cesta()

    if not datos_cesta or not datos_cesta["productos_cesta"]:
        return redirect("/compras")

    usuario = Usuario.query.get(id_usuario)
    
    if not usuario:
        return redirect(url_for('login'))

    nuevo_pedido = Pedido(
        id_usuario=id_usuario,
        nombre_envio=usuario.nombre, 
        apellido1_envio=usuario.apellido1, 
        apellido2_envio=usuario.apellido2,
        fecha=datetime.utcnow(),
        estado="pendiente",
        tipo_pedido="domicilio"
    )
    db.session.add(nuevo_pedido)
    db.session.commit()  # Commit para guardar el pedido y obtener su id_pedido

    total = sum(Decimal(producto["precio_unitario"]) * producto["cantidad"] for producto in datos_cesta["productos_cesta"])

    for producto in datos_cesta["productos_cesta"]:
        pedido_producto = PedidoProducto(
            id_pedido=nuevo_pedido.id_pedido,  # Ahora el id_pedido está disponible
            id_variante=producto["variante"]["id_variante"],
            cantidad=producto["cantidad"],
            total_producto=producto["subtotal"]
        )
        db.session.add(pedido_producto)

    cesta = Cesta.query.filter_by(id_usuario=id_usuario).first()
    if cesta:
        CestaProducto.query.filter_by(id_cesta=cesta.id_cesta).delete()

    db.session.commit()

    return redirect(url_for('compras'))
