from flask import render_template, request
from math import ceil
from backend.supabase_rest import select

def catalogo():
    nombre_seccion = request.args.get('seccion', None)
    nombre_categoria = request.args.get('categoria', None)
    pagina_actual = request.args.get('pagina', 1, type=int)
    productos_por_pagina = 42

    params = {
        "select": "id_producto,nombre_producto,precio,id_variante,color,img_color,imagen_url,seccion,nombre_categoria",
        "order": "id_producto.asc",
    }
    if nombre_seccion:
        params["seccion"] = f"eq.{nombre_seccion}"
    if nombre_categoria:
        params["nombre_categoria"] = f"eq.{nombre_categoria}"

    filas = select("vista_productos_completa", params)

    # Fallback: si la vista completa no devuelve filas, usar tablas base
    if not filas:
        base = select("productos", {"select": "id_producto,nombre,precio,id_seccion", "order": "id_producto.asc"})
        secciones = select("secciones", {"select": "id_seccion,nombre"})
        secciones_map = {s.get("id_seccion"): s.get("nombre") for s in secciones}

        if nombre_seccion:
            base = [p for p in base if secciones_map.get(p.get("id_seccion")) == nombre_seccion]

        if nombre_categoria:
            categorias = select("categorias", {"select": "id_categoria,nombre"})
            cat_ids = {c.get("id_categoria") for c in categorias if c.get("nombre") == nombre_categoria}
            rel = select("productos_categorias", {"select": "id_producto,id_categoria"})
            permitidos = {r.get("id_producto") for r in rel if r.get("id_categoria") in cat_ids}
            base = [p for p in base if p.get("id_producto") in permitidos]

        variantes = select("productos_variantes", {"select": "id_producto,id_variante,id_color"})
        colores = select("colores", {"select": "id_color,color,img_color"})
        colores_map = {c.get("id_color"): c for c in colores}
        imagenes = select("productos_imagenes_colores", {"select": "id_producto,id_color,imagen_url"})

        filas = []
        for p in base:
            pid = p.get("id_producto")
            vars_pid = [v for v in variantes if v.get("id_producto") == pid]
            imgs_pid = [i for i in imagenes if i.get("id_producto") == pid]

            if not vars_pid:
                # Producto sin variantes: mantenerlo visible
                filas.append({
                    "id_producto": pid,
                    "nombre_producto": p.get("nombre", ""),
                    "precio": p.get("precio", 0),
                    "id_variante": None,
                    "id_color": None,
                    "color": None,
                    "img_color": None,
                    "imagen_url": imgs_pid[0].get("imagen_url") if imgs_pid else None,
                })
                continue

            for v in vars_pid:
                color = colores_map.get(v.get("id_color"), {})
                img = next((x.get("imagen_url") for x in imgs_pid if x.get("id_color") == v.get("id_color")), None)
                filas.append({
                    "id_producto": pid,
                    "nombre_producto": p.get("nombre", ""),
                    "precio": p.get("precio", 0),
                    "id_variante": v.get("id_variante"),
                    "id_color": v.get("id_color"),
                    "color": color.get("color"),
                    "img_color": color.get("img_color"),
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

    productos_all = list(productos_map.values())
    total_paginas = max(1, ceil(len(productos_all) / productos_por_pagina)) if productos_all else 0
    inicio = (pagina_actual - 1) * productos_por_pagina
    fin = inicio + productos_por_pagina
    productos = productos_all[inicio:fin]

    return render_template(
        'productos/catalogo.html',
        productos=productos,
        pagina_actual=pagina_actual,
        total_paginas=total_paginas,
        nombre_seccion=nombre_seccion,
        nombre_categoria=nombre_categoria,
    )
