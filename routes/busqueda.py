from flask import render_template, request
from math import ceil
from backend.Modelos.database import db
from backend.Modelos import Producto  # Asegúrate de importar tu modelo Producto

def busqueda():
    # Se obtiene el parámetro 'busqueda' de la URL, que es el término que el usuario busca
    busqueda = request.args.get('busqueda', '')  # Obtiene el parámetro 'busqueda'

    # Si no se proporciona un término de búsqueda, se renderiza la página de búsqueda vacía
    if not busqueda:
        return render_template('components/busqueda.html', busqueda=busqueda)

    # Se obtiene el número de la página actual
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    # Construimos la consulta base con filtro por nombre de producto
    query = db.session.query(Producto).filter(Producto.nombre.ilike(f"%{busqueda}%"))
    

    # Realiza la paginación de la consulta
    productos_paginados = query.order_by(Producto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)


    # Calcular el total de páginas
    total_paginas = ceil(query.count() / productos_por_pagina)

    # Si no se encuentran productos, renderiza un mensaje adecuado
    if not productos_paginados.items:
        return render_template(
            'components/busqueda.html',
            busqueda=busqueda,
            mensaje="No se encontraron productos que coincidan con tu búsqueda."
        )

    # Si se encontraron productos, renderiza la vista de resultados de búsqueda
    return render_template(
        'components/busqueda.html',
        productos=productos_paginados.items,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        busqueda=busqueda
    )
