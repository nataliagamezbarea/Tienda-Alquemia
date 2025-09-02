from flask import render_template, request
from math import ceil
from backend.Modelos import Producto
from backend.Modelos.Seccion import Seccion
from backend.Modelos.Categoria import Categoria
from backend.Modelos.ProductoCategoria import ProductoCategoria
from backend.Modelos.database import db

def catalogo():
    nombre_seccion = request.args.get('seccion', None)
    nombre_categoria = request.args.get('categoria', None)
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    # Consulta base
    query = db.session.query(Producto).join(Seccion).join(ProductoCategoria).join(Categoria)
    if nombre_seccion:
        query = query.filter(Seccion.nombre == nombre_seccion)
    if nombre_categoria:
        query = query.filter(Categoria.nombre == nombre_categoria)
    query = query.distinct(Producto.id_producto)

    # Paginación
    productos_paginados = query.order_by(Producto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)
    productos = productos_paginados.items

    # Cargar variantes y relaciones, y asignar imágenes principal y hover
    for producto in productos:
        producto.variantes = producto.variantes
        producto.imagen_principal = producto.imagenes[0].imagen_url if producto.imagenes else ''
        producto.imagen_hover = producto.imagenes[1].imagen_url if len(producto.imagenes) > 1 else producto.imagen_principal

    total_paginas = ceil(query.count() / productos_por_pagina)

    return render_template(
        'productos/catalogo.html',
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        nombre_seccion=nombre_seccion,
        nombre_categoria=nombre_categoria,
    )
