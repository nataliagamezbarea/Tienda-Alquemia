from flask import session
from backend.supabase_rest import select

def obtener_cesta():
    # Fallback seguro para no romper la navegación si no hay Postgres directo
    if not session.get("user"):
        return {"productos_cesta": [], "numero_de_productos": 0, "total": 0.00}

    id_usuario = session.get("id_usuario") or session.get("user")
    if not id_usuario:
        return {"productos_cesta": [], "numero_de_productos": 0, "total": 0.00}

    # Obtener la cesta del usuario
    cestas = select("cestas", {"id_usuario": f"eq.{id_usuario}"})

    if not cestas:
        return {"productos_cesta": [], "numero_de_productos": 0, "total": 0.00}

    id_cesta = cestas[0].get("id_cesta")

    # Obtener productos en la cesta
    cesta_productos = select("cestas_productos", {"id_cesta": f"eq.{id_cesta}"})

    if not cesta_productos:
        return {"productos_cesta": [], "numero_de_productos": 0, "total": 0.00}

    productos_cesta = []
    total = 0.0
    numero_productos = 0

    for cp in cesta_productos:
        id_variante = cp.get("id_variante")
        cantidad = cp.get("cantidad", 1)

        # Obtener detalles de la variante
        variantes = select("productos_variantes", {"id_variante": f"eq.{id_variante}"})
        if not variantes:
            continue

        variante = variantes[0]
        id_producto = variante.get("id_producto")

        # Obtener detalles del producto
        productos = select("productos", {"id_producto": f"eq.{id_producto}"})
        if not productos:
            continue

        producto = productos[0]

        # Obtener color y talla
        colores = select("colores", {"id_color": f"eq.{variante.get('id_color')}"}) if variante.get("id_color") else []
        tallas = select("tallas", {"id_talla": f"eq.{variante.get('id_talla')}"}) if variante.get("id_talla") else []

        color_nombre = colores[0].get("color") if colores else "Sin color"
        talla_nombre = tallas[0].get("talla") if tallas else "Sin talla"

        imagenes = select(
            "productos_imagenes_colores",
            {
                "select": "imagen_url",
                "id_producto": f"eq.{id_producto}",
                "id_color": f"eq.{variante.get('id_color')}",
                "limit": "1",
            },
        )
        imagen_url = imagenes[0].get("imagen_url") if imagenes else "/static/img/placeholder.jpg"

        precio = float(producto.get("precio", 0))
        subtotal = precio * cantidad
        total += subtotal
        numero_productos += cantidad

        productos_cesta.append({
            "id_producto": id_producto,
            "nombre": producto.get("nombre", ""),
            "imagen_url": imagen_url,
            "variante": {
                "id_variante": id_variante,
                "color": color_nombre,
                "talla": talla_nombre,
            },
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

    return {
        "productos_cesta": productos_cesta,
        "numero_de_productos": numero_productos,
        "total": round(total, 2)
    }
