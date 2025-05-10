from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import os

from backend.Modelos import (
    Producto, ProductoVariante, ProductoCategoria, ProductoImagen,
    Talla, Color, Seccion, Categoria
)
from backend.Modelos.database import db

# Verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Guardar imagen y devolver ruta relativa
def guardar_imagen(imagen):
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        imagen.save(filepath)
        return f'/static/uploads/{filename}'
    return None


# Obtener productos y renderizar HTML
def obtener_productos_html():
    productos = Producto.query.all()
    productos_dict = {}

    for producto in productos:
        pid = producto.id_producto
        productos_dict[pid] = {
            'id_producto': pid,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'variantes': [],
            'imagenes': [],
            'categorias': ', '.join([c.nombre for c in producto.categorias]),
            'colores': set(),
            'tallas': set(),
            'secciones': producto.seccion.nombre if producto.seccion else '',
            'stock_total': 0,
        }

        for variante in producto.variantes:
            productos_dict[pid]['variantes'].append({
                'color': variante.color.color,
                'talla': variante.talla.talla,
                'stock': variante.stock
            })
            productos_dict[pid]['colores'].add(variante.color.color)
            productos_dict[pid]['tallas'].add(variante.talla.talla)
            productos_dict[pid]['stock_total'] += variante.stock

        for imagen in producto.imagenes:
            productos_dict[pid]['imagenes'].append({
                'imagen_url': imagen.imagen_url,
                'color': imagen.color.color
            })

        productos_dict[pid]['colores'] = ', '.join(productos_dict[pid]['colores'])
        productos_dict[pid]['tallas'] = ', '.join(productos_dict[pid]['tallas'])

    productos_ordenados = sorted(productos_dict.values(), key=lambda x: x['precio'], reverse=True)

    secciones = [(s.id_seccion, s.nombre) for s in Seccion.query.all()]
    colores = [(c.id_color, c.color) for c in Color.query.all()]
    tallas = [(t.id_talla, t.talla) for t in Talla.query.all()]
    categorias = [(c.id_categoria, c.nombre) for c in Categoria.query.all()]

    return render_template(
        'admin/productos.html',
        productos=productos_ordenados,
        secciones=secciones,
        colores=colores,
        tallas=tallas,
        categorias=categorias
    )
