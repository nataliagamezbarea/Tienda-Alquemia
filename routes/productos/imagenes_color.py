from flask import jsonify
from backend.Modelos import ProductoImagen
from backend.Modelos.database import db

def imagenes_color(id_producto, id_color):
    # Traer solo las imágenes de ese producto y color
    imagenes = (
        db.session.query(ProductoImagen)
        .filter_by(id_producto=id_producto, id_color=id_color)
        .all()
    )
    urls = [img.imagen_url for img in imagenes if img.imagen_url]
    return jsonify(urls)
