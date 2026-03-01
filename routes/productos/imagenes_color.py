from flask import jsonify
from backend.supabase_rest import select

def imagenes_color(id_producto, id_color):
    filas = select(
        "productos_imagenes_colores",
        {
            "select": "imagen_url",
            "id_producto": f"eq.{id_producto}",
            "id_color": f"eq.{id_color}",
            "order": "id_imagen.asc",
        },
    )
    urls = [f.get("imagen_url") for f in filas if f.get("imagen_url")]
    return jsonify(urls)
