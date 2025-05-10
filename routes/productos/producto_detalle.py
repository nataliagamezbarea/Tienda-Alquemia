from flask import render_template, request
from sqlalchemy.orm import joinedload
from backend.Modelos import Producto, ProductoVariante
from backend.Modelos.database import db

def producto_detalle(id_producto):
    producto = db.session.query(Producto).\
        options(
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.color),
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.talla),
            joinedload(Producto.imagenes),
            joinedload(Producto.categorias)
        ).\
        filter(Producto.id_producto == id_producto).\
        first()

    if not producto:
        return "Producto no encontrado", 404

    imagenes_por_color = {}
    for imagen in producto.imagenes:
        if imagen.id_color not in imagenes_por_color:
            imagenes_por_color[imagen.id_color] = []
        imagenes_por_color[imagen.id_color].append(imagen.imagen_url)

    categorias_ids = [categoria.id_categoria for categoria in producto.categorias]

    # --- ⚡ Backend corregido para productos recomendados
    productos_recomendados = db.session.query(Producto).\
        options(
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.color),
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.talla),
            joinedload(Producto.imagenes),
            joinedload(Producto.categorias),
            joinedload(Producto.seccion)  # <-- añadido por compatibilidad
        ).\
        join(Producto.categorias).\
        filter(
            Producto.id_producto != id_producto,
            Producto.imagenes.any(),
            Producto.categorias.any(Producto.categorias.property.mapper.class_.id_categoria.in_(categorias_ids))
        ).\
        distinct().\
        limit(4).\
        all()

    # --- ⚡ Normalizar imágenes para productos recomendados
    for prod in productos_recomendados:
        imagenes_validas = [img for img in prod.imagenes if hasattr(img, 'imagen_url') and img.imagen_url]

        if len(imagenes_validas) == 0:
            # Añadir dos placeholders si no hay imágenes
            placeholder = type('MockImage', (object,), {'imagen_url': '/static/img/placeholder.jpg'})()
            imagenes_validas = [placeholder, placeholder]
        elif len(imagenes_validas) == 1:
            # Duplicar si solo hay una imagen
            imagenes_validas.append(imagenes_validas[0])

        # Reemplazamos imágenes antiguas
        prod.imagenes = imagenes_validas

    # Verifica si se pasó el color y la talla en el formulario POST
    id_color = request.form.get('id_color', None)
    id_talla = request.form.get('id_talla', None)

    # Si se recibieron el color y la talla, buscar la variante
    id_variante = None
    if id_color and id_talla:
        id_variante = db.session.query(ProductoVariante).\
            filter_by(id_producto=id_producto, id_color=id_color, id_talla=id_talla).\
            first()

        if id_variante:
            id_variante = id_variante.id_variantes

    return render_template(
        'productos/producto_detalle.html',
        producto=producto,
        imagenes_por_color=imagenes_por_color,
        productos=productos_recomendados,
        id_variante=id_variante  # Pasamos el id_variante a la plantilla
    )
