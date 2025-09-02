from flask import render_template, request, redirect, session, url_for, current_app
from sqlalchemy.orm import joinedload
from math import ceil

from backend.Modelos import (
    Producto, ProductoVariante, ProductoCategoria, ProductoImagen,
    Talla, Color, Seccion, Categoria
)
from backend.Modelos.database import db

def obtener_productos_html():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 50

    query = db.session.query(Producto).options(
        joinedload(Producto.variantes).joinedload(ProductoVariante.color),
        joinedload(Producto.variantes).joinedload(ProductoVariante.talla),
        joinedload(Producto.imagenes).joinedload(ProductoImagen.color),
        joinedload(Producto.categorias),
        joinedload(Producto.seccion)
    )

    # Orden descendente por id_producto para mostrar los más recientes primero
    productos_paginados = query.order_by(Producto.id_producto.desc()).paginate(page=pagina_actual, per_page=productos_por_pagina, error_out=False)
    productos = productos_paginados.items

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

    # No ordenar aquí, ya está ordenado desde el query
    productos_ordenados = list(productos_dict.values())

    secciones = [(s.id_seccion, s.nombre) for s in Seccion.query.all()]
    colores = [(c.id_color, c.color) for c in Color.query.all()]
    tallas = [(t.id_talla, t.talla) for t in Talla.query.all()]
    categorias = [(c.id_categoria, c.nombre) for c in Categoria.query.all()]

    total_paginas = ceil(query.count() / productos_por_pagina)

    return render_template(
        'admin/productos/productos.html',
        productos=productos_ordenados,
        secciones=secciones,
        colores=colores,
        tallas=tallas,
        categorias=categorias,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas
    )
