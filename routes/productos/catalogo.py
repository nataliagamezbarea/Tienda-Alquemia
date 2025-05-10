from flask import render_template, request
from sqlalchemy.orm import joinedload
from backend.Modelos import Producto
from backend.Modelos.Seccion import Seccion
from backend.Modelos.Categoria import Categoria
from backend.Modelos.ProductoCategoria import ProductoCategoria
from math import ceil
from backend.Modelos.database import db

def catalogo():
    # Obtiene el parámetro 'seccion' de la URL, si no se pasa, usa 'hombre' por defecto
    nombre_seccion = request.args.get('seccion', None)
    nombre_categoria = request.args.get('categoria', None)
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    # Construir la consulta base
    query = db.session.query(Producto).\
        join(Seccion).\
        join(ProductoCategoria).\
        join(Categoria)

    # Filtrar por seccion y categoria si se pasa
    if nombre_seccion:
        query = query.filter(Seccion.nombre == nombre_seccion)
    if nombre_categoria:
        query = query.filter(Categoria.nombre == nombre_categoria)

    # Obtener productos únicos (evitar duplicados)
    query = query.distinct(Producto.id_producto)

    # Realiza la consulta paginada
    productos_paginados = query.order_by(Producto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)

    # Obtener las imágenes y variantes de los productos de manera separada
    productos = productos_paginados.items
    for producto in productos:
        producto.imagenes = producto.imagenes  # Esto debería cargar las imágenes de manera eficiente
        producto.variantes = producto.variantes  # Esto carga las variantes si es necesario

    # Calcular el total de páginas
    total_paginas = ceil(query.count() / productos_por_pagina)

    return render_template(
        'productos/catalogo.html',
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        nombre_seccion=nombre_seccion,
        nombre_categoria=nombre_categoria
    )
