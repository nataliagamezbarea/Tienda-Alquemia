from flask import render_template, request
from sqlalchemy.orm import joinedload
from backend.Modelos import Producto, ProductoVariante
from backend.Modelos.database import db

def producto_detalle(id_producto):
    # --- Cargar producto con todas sus relaciones necesarias
    producto = (
        db.session.query(Producto)
        .options(
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.color),
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.talla),
            joinedload(Producto.imagenes),
            joinedload(Producto.categorias)
        )
        .filter(Producto.id_producto == id_producto)
        .first()
    )

    if not producto:
        return "Producto no encontrado", 404

    # --- Organizar imágenes por color
    imagenes_por_color = {}
    for imagen in producto.imagenes:
        color_id = imagen.id_color or 0  # Por si hay imágenes sin color
        imagenes_por_color.setdefault(color_id, []).append(imagen.imagen_url)

    # --- IDs de categorías del producto actual
    categorias_ids = [c.id_categoria for c in producto.categorias]

    # --- Productos recomendados: mismos IDs de categorías, excluyendo el actual
    productos_recomendados = (
        db.session.query(Producto)
        .options(
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.color),
            joinedload(Producto.variantes).joinedload(Producto.variantes.property.mapper.class_.talla),
            joinedload(Producto.imagenes),
            joinedload(Producto.categorias)
        )
        .join(Producto.categorias)
        .filter(
            Producto.id_producto != id_producto,
            Producto.categorias.any(Producto.categorias.property.mapper.class_.id_categoria.in_(categorias_ids)),
            Producto.imagenes.any()
        )
        .distinct()
        .limit(4)
        .all()
    )

    # --- Normalizar imágenes de productos recomendados
    for prod in productos_recomendados:
        valid_imgs = [img for img in prod.imagenes if getattr(img, 'imagen_url', None)]
        if not valid_imgs:
            placeholder = type('MockImage', (object,), {'imagen_url': '/static/img/placeholder.jpg'})()
            prod.imagenes = [placeholder, placeholder]
        elif len(valid_imgs) == 1:
            prod.imagenes = [valid_imgs[0], valid_imgs[0]]
        else:
            prod.imagenes = valid_imgs

    # --- Buscar variante seleccionada si se envió POST
    id_variante = None
    id_color = request.form.get('id_color')
    id_talla = request.form.get('id_talla')
    if id_color and id_talla:
        variante = db.session.query(ProductoVariante).filter_by(
            id_producto=id_producto,
            id_color=id_color,
            id_talla=id_talla
        ).first()
        if variante:
            id_variante = variante.id_variante

    return render_template(
        'productos/producto_detalle.html',
        producto=producto,
        imagenes_por_color=imagenes_por_color,
        productos=productos_recomendados,
        id_variante=id_variante
    )
