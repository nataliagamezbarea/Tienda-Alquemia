from flask import render_template, redirect, url_for, session
from backend.supabase_rest import select, insert, _request
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

    usuarios = select("usuarios", {"select": "id_usuario,nombre,apellido1,apellido2", "id_usuario": f"eq.{id_usuario}", "limit": "1"})
    usuario = usuarios[0] if usuarios else None
    
    if not usuario:
        return redirect(url_for('login'))

    nuevo_pedido = insert(
        "pedidos",
        {
            "id_usuario": id_usuario,
            "nombre_envio": usuario.get("nombre"),
            "apellido1_envio": usuario.get("apellido1"),
            "apellido2_envio": usuario.get("apellido2") or "",
            "fecha": datetime.utcnow().date().isoformat(),
            "estado": "pendiente",
            "tipo_pedido": "domicilio",
        },
    )
    if not nuevo_pedido:
        return redirect(url_for('compras'))

    id_pedido = nuevo_pedido[0].get("id_pedido")

    total = sum(Decimal(str(producto["precio"])) * producto["cantidad"] for producto in datos_cesta["productos_cesta"])

    lineas = []
    for producto in datos_cesta["productos_cesta"]:
        lineas.append(
            {
                "id_pedido": id_pedido,
                "id_variante": producto["variante"]["id_variante"],
                "cantidad": producto["cantidad"],
                "total_producto": producto["subtotal"],
            }
        )

    if lineas:
        insert("pedidos_productos", lineas)

    cestas = select("cestas", {"select": "id_cesta", "id_usuario": f"eq.{id_usuario}", "limit": "1"})
    if cestas:
        _request("DELETE", "cestas_productos", params={"id_cesta": f"eq.{cestas[0].get('id_cesta')}"})

    return redirect(url_for('compras'))
