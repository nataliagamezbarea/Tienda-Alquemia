from flask import render_template, request
from sqlalchemy.orm import joinedload
from backend.Modelos import Producto
from backend.Modelos.Seccion import Seccion
from backend.Modelos.Categoria import Categoria
from backend.Modelos.ProductoCategoria import ProductoCategoria
from backend.Modelos.database import db
from math import ceil

def catalogo():
    nombre_seccion = request.args.get('seccion', None)
    nombre_categoria = request.args.get('categoria', None)
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    # Consulta base solo productos
    query = db.session.query(Producto).options(
        joinedload(Producto.imagenes),    # Eager loading imágenes
        joinedload(Producto.variantes)    # Eager loading variantes
    )

    # Filtrar productos por seccion y categoria mediante joins y filtros
    if nombre_seccion:
        query = query.join(Producto.seccion).filter(Seccion.nombre == nombre_seccion)
    if nombre_categoria:
        query = query.join(Producto.categorias).filter(Categoria.nombre == nombre_categoria)

    # Conteo total sin joins innecesarios para evitar sobrecarga
    total_productos = query.with_entities(Producto.id_producto).distinct().count()

    # Paginación con offset y limit
    productos = query.order_by(Producto.id_producto).offset((pagina_actual - 1) * productos_por_pagina).limit(productos_por_pagina).all()

    total_paginas = ceil(total_productos / productos_por_pagina) if total_productos else 1

    return render_template(
        'productos/catalogo.html',
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        nombre_seccion=nombre_seccion,
        nombre_categoria=nombre_categoria
    )
