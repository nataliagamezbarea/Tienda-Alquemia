from flask import redirect, render_template, request, url_for
from math import ceil
from backend.Modelos.database import db
from backend.Vistas.VistaProductoCompleto import VistaProductoCompleto  # Importamos la vista de los productos completos

def busqueda():
    # Se obtiene el parámetro 'busqueda' de la URL, que es el término que el usuario busca
    busqueda = request.args.get('busqueda', '')  # Obtiene el parámetro 'busqueda'
    
    # Si no se proporciona un término de búsqueda, se renderiza la página de búsqueda vacía
    if not busqueda:
        return render_template('components/busqueda.html', busqueda=busqueda)  # Pasa la busqueda a la plantilla
    
    # Se obtiene el número de la página actual, por defecto es la página 1
    pagina_actual = request.args.get('pagina', 1, type=int)
    
    # Definimos cuántos productos queremos mostrar por página
    productos_por_pagina = 42

    # Construimos la consulta base para obtener los productos desde la vista
    query = db.session.query(VistaProductoCompleto).filter(VistaProductoCompleto.nombre_producto.ilike(f"%{busqueda}%"))

    # Ejecutamos la consulta y paginamos los resultados según la página actual y el número de productos por página
    productos_paginados = query.order_by(VistaProductoCompleto.id_producto).paginate(page=pagina_actual, per_page=productos_por_pagina)

    # Calculamos el total de páginas a partir del número total de productos y productos por página
    total_paginas = ceil(query.count() / productos_por_pagina)

    # Finalmente, renderizamos la plantilla de búsqueda con los resultados y la información de la paginación
    return render_template(
        'components/busqueda.html',  
        productos=productos_paginados.items,  # Pasamos los productos de la página actual
        pagina_actual=pagina_actual,  # Pasamos la página actual
        total_paginas=total_paginas,  # Pasamos el total de páginas
        busqueda=busqueda  # Pasamos el término de búsqueda para mostrarlo en la plantilla
    )
