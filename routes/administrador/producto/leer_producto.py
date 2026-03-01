from flask import render_template, request, redirect, session, url_for
from math import ceil
from backend.supabase_rest import select

def obtener_productos_html():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 50
    offset = (pagina_actual - 1) * productos_por_pagina

    productos = select(
        "productos",
        {
            "select": "id_producto,nombre,precio,descripcion,id_seccion",
            "order": "id_producto.desc",
            "limit": str(productos_por_pagina),
            "offset": str(offset),
        },
    )

    total_productos = len(select("productos", {"select": "id_producto"}))
    total_paginas = ceil(total_productos / productos_por_pagina) if total_productos else 1

    secciones_rows = select("secciones", {"select": "id_seccion,nombre"})
    colores_rows = select("colores", {"select": "id_color,color"})
    tallas_rows = select("tallas", {"select": "id_talla,talla"})
    categorias_rows = select("categorias", {"select": "id_categoria,nombre"})

    seccion_map = {s.get("id_seccion"): s.get("nombre", "") for s in secciones_rows}
    color_map = {c.get("id_color"): c.get("color", "") for c in colores_rows}
    talla_map = {t.get("id_talla"): t.get("talla", "") for t in tallas_rows}
    categoria_map = {c.get("id_categoria"): c.get("nombre", "") for c in categorias_rows}

    producto_ids = [p.get("id_producto") for p in productos if p.get("id_producto") is not None]
    variantes = []
    imagenes = []
    productos_categorias = []
    if producto_ids:
        in_ids = ",".join(str(pid) for pid in producto_ids)
        variantes = select(
            "productos_variantes",
            {
                "select": "id_producto,id_color,id_talla,stock",
                "id_producto": f"in.({in_ids})",
            },
        )
        imagenes = select(
            "productos_imagenes_colores",
            {
                "select": "id_producto,id_color,imagen_url",
                "id_producto": f"in.({in_ids})",
            },
        )
        productos_categorias = select(
            "productos_categorias",
            {
                "select": "id_producto,id_categoria",
                "id_producto": f"in.({in_ids})",
            },
        )

    productos_dict = {}

    for producto in productos:
        pid = producto.get("id_producto")
        productos_dict[pid] = {
            'id_producto': pid,
            'nombre': producto.get("nombre", ""),
            'descripcion': producto.get("descripcion", ""),
            'precio': float(producto.get("precio", 0) or 0),
            'variantes': [],
            'imagenes': [],
            'categorias': '',
            'colores': set(),
            'tallas': set(),
            'secciones': seccion_map.get(producto.get("id_seccion"), ''),
            'stock_total': 0,
        }

        for variante in [v for v in variantes if v.get("id_producto") == pid]:
            color_nombre = color_map.get(variante.get("id_color"), "")
            talla_nombre = talla_map.get(variante.get("id_talla"), "")
            stock = int(variante.get("stock", 0) or 0)
            productos_dict[pid]['variantes'].append({
                'color': color_nombre,
                'talla': talla_nombre,
                'stock': stock
            })
            if color_nombre:
                productos_dict[pid]['colores'].add(color_nombre)
            if talla_nombre:
                productos_dict[pid]['tallas'].add(talla_nombre)
            productos_dict[pid]['stock_total'] += stock

        for imagen in [i for i in imagenes if i.get("id_producto") == pid]:
            productos_dict[pid]['imagenes'].append({
                'imagen_url': imagen.get("imagen_url"),
                'color': color_map.get(imagen.get("id_color"), "")
            })

        categorias_nombres = []
        for pc in [r for r in productos_categorias if r.get("id_producto") == pid]:
            nombre_cat = categoria_map.get(pc.get("id_categoria"))
            if nombre_cat:
                categorias_nombres.append(nombre_cat)
        productos_dict[pid]['categorias'] = ', '.join(sorted(set(categorias_nombres)))

        productos_dict[pid]['colores'] = ', '.join(sorted(productos_dict[pid]['colores']))
        productos_dict[pid]['tallas'] = ', '.join(sorted(productos_dict[pid]['tallas']))

    # No ordenar aquí, ya está ordenado desde el query
    productos_ordenados = list(productos_dict.values())

    secciones = secciones_rows
    colores = colores_rows
    tallas = tallas_rows
    categorias = categorias_rows

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
