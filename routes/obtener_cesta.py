from flask import session
from backend.Modelos.Cesta import Cesta
from backend.Modelos.CestaProducto import CestaProducto
from backend.Vistas.VistaProductoCompleto import VistaProductoCompleto
from decimal import Decimal

def obtener_cesta():
    # Obtener el ID del usuario desde la sesión
    id_usuario = session.get("user")
    if not id_usuario:
        return None  # Si no hay usuario logueado, retornamos None

    # Buscar la cesta del usuario
    cesta = Cesta.query.filter_by(id_usuario=id_usuario).first()
    if not cesta:
        return {
            "productos_cesta": [],
            "numero_de_productos": 0,
            "total": 0.00
        }

    # Obtener los productos en la cesta
    productos_en_cesta = CestaProducto.query.filter_by(id_cesta=cesta.id_cesta).all()
    ids_variante = [producto.id_variante for producto in productos_en_cesta]

    # Consultar los datos completos desde la vista
    productos_vista = {
        producto.id_variante: producto
        for producto in VistaProductoCompleto.query.filter(
            VistaProductoCompleto.id_variante.in_(ids_variante)
        ).all()
    }

    # Generar lista de productos con comprensión de listas
    lista_productos = [
        {
            "id_producto": vista.id_producto,
            "nombre": vista.nombre_producto,
            "precio_unitario": float(vista.precio),
            "cantidad": producto.cantidad,
            "subtotal": round(float(Decimal(vista.precio) * producto.cantidad), 2),
            "imagen_url": vista.imagen_url,
            "variante": {
                "id_variante": vista.id_variante,
                "descripcion": vista.descripcion,
                "color": vista.color,
                "talla": vista.talla
            }
        }
        for producto in productos_en_cesta
        if (vista := productos_vista.get(producto.id_variante)) is not None
    ]

    # Calcular el total de la cesta
    total = sum(Decimal(p["precio_unitario"]) * p["cantidad"] for p in lista_productos)

    return {
        "productos_cesta": lista_productos,
        "numero_de_productos": sum(p["cantidad"] for p in lista_productos),
        "total": round(float(total), 2)
    }
