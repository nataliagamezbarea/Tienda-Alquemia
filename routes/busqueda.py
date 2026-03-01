from flask import render_template, request
from math import ceil
from backend.supabase_rest import select

def busqueda():
    # Se obtiene el parámetro 'busqueda' de la URL, que es el término que el usuario busca
    busqueda = request.args.get('busqueda', '')  # Obtiene el parámetro 'busqueda'

    # Si no se proporciona un término de búsqueda, se renderiza la página de búsqueda vacía
    if not busqueda:
        return render_template('components/busqueda.html', busqueda=busqueda)

    # Se obtiene el número de la página actual
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    filas = select(
        "vista_productos_completa",
        {
            "select": "id_producto,nombre_producto,precio,id_variante,color,img_color,imagen_url",
            "nombre_producto": f"ilike.*{busqueda}*",
            "order": "id_producto.asc",
        },
    )

    if not filas:
        base = select(
            "productos",
            {
                "select": "id_producto,nombre,precio",
                "nombre": f"ilike.*{busqueda}*",
                "order": "id_producto.asc",
            },
        )
        vars_all = select("productos_variantes", {"select": "id_producto,id_variante,id_color"})
        imgs_all = select("productos_imagenes_colores", {"select": "id_producto,id_color,imagen_url"})
        cols_all = select("colores", {"select": "id_color,color,img_color"})
        c_map = {c.get("id_color"): c for c in cols_all}

        filas = []
        for p in base:
            pid = p.get("id_producto")
            vars_pid = [v for v in vars_all if v.get("id_producto") == pid]
            imgs_pid = [i for i in imgs_all if i.get("id_producto") == pid]
            if not vars_pid:
                filas.append({
                    "id_producto": pid,
                    "nombre_producto": p.get("nombre"),
                    "precio": p.get("precio"),
                    "id_variante": None,
                    "color": None,
                    "img_color": None,
                    "imagen_url": imgs_pid[0].get("imagen_url") if imgs_pid else None,
                })
                continue

            for v in vars_pid:
                c = c_map.get(v.get("id_color"), {})
                img = next((x.get("imagen_url") for x in imgs_pid if x.get("id_color") == v.get("id_color")), None)
                filas.append({
                    "id_producto": pid,
                    "nombre_producto": p.get("nombre"),
                    "precio": p.get("precio"),
                    "id_variante": v.get("id_variante"),
                    "color": c.get("color"),
                    "img_color": c.get("img_color"),
                    "imagen_url": img,
                })

    colores_lista = select("colores", {"select": "id_color,color"})
    color_to_id = {c.get("color"): c.get("id_color") for c in colores_lista if c.get("color") is not None}

    productos_map = {}
    for f in filas:
        pid = f.get("id_producto")
        if pid is None:
            continue

        p = productos_map.get(pid)
        if not p:
            p = {
                "id_producto": pid,
                "nombre": f.get("nombre_producto", ""),
                "precio": f.get("precio", 0),
                "imagenes": [],
                "variantes": [],
            }
            productos_map[pid] = p

        img = f.get("imagen_url")
        if img and not any(i.get("imagen_url") == img for i in p["imagenes"]):
            p["imagenes"].append({"imagen_url": img})

        id_variante = f.get("id_variante")
        id_color = color_to_id.get(f.get("color"))
        if id_variante is not None and id_color is not None:
            if not any(v.get("id_variante") == id_variante for v in p["variantes"]):
                p["variantes"].append(
                    {
                        "id_variante": id_variante,
                        "color": {
                            "id_color": id_color,
                            "img_color": f.get("img_color"),
                            "color": f.get("color"),
                        },
                    }
                )

    productos = list(productos_map.values())
    total_paginas = max(1, ceil(len(productos) / productos_por_pagina)) if productos else 0
    inicio = (pagina_actual - 1) * productos_por_pagina
    fin = inicio + productos_por_pagina
    productos_pagina = productos[inicio:fin]

    # Si no se encuentran productos, renderiza un mensaje adecuado
    if not productos_pagina:
        return render_template(
            'components/busqueda.html',
            busqueda=busqueda,
            mensaje="No se encontraron productos que coincidan con tu búsqueda."
        )

    # Si se encontraron productos, renderiza la vista de resultados de búsqueda
    return render_template(
        'components/busqueda.html',
        productos=productos_pagina,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        busqueda=busqueda
    )
