from flask import render_template, request
from backend.supabase_rest import select

def producto_detalle(id_producto):
    filas = select(
        "vista_productos_completa",
        {
            "select": "id_producto,nombre_producto,precio,descripcion,id_categoria,nombre_categoria,id_variante,color,img_color,talla,imagen_url,seccion",
            "id_producto": f"eq.{id_producto}",
            "order": "id_variante.asc",
        },
    )

    colores_lista = select("colores", {"select": "id_color,color,img_color"})
    color_to_id = {c.get("color"): c.get("id_color") for c in colores_lista if c.get("color") is not None}
    tallas_lista = select("tallas", {"select": "id_talla,talla"})
    talla_to_id = {t.get("talla"): t.get("id_talla") for t in tallas_lista if t.get("talla") is not None}

    # Si la vista no expone id_talla, lo reconstruimos por nombre de talla.
    for f in filas:
        if f.get("id_talla") is None:
            f["id_talla"] = talla_to_id.get(f.get("talla"))

    if not filas:
        base_rows = select(
            "productos",
            {
                "select": "id_producto,nombre,precio,descripcion",
                "id_producto": f"eq.{id_producto}",
                "limit": "1",
            },
        )
        if not base_rows:
            return "Producto no encontrado", 404

        base_p = base_rows[0]
        vars_all = select("productos_variantes", {"select": "id_variante,id_producto,id_color,id_talla"})
        imgs_all = select("productos_imagenes_colores", {"select": "id_producto,id_color,imagen_url"})
        t_map = {t.get("id_talla"): t.get("talla") for t in tallas_lista}
        rel = select("productos_categorias", {"select": "id_producto,id_categoria"})
        cats = select("categorias", {"select": "id_categoria,nombre"})
        cat_map = {c.get("id_categoria"): c.get("nombre") for c in cats}

        vars_pid = [v for v in vars_all if v.get("id_producto") == id_producto]
        imgs_pid = [i for i in imgs_all if i.get("id_producto") == id_producto]
        cats_pid = [r.get("id_categoria") for r in rel if r.get("id_producto") == id_producto]

        for v in vars_pid if vars_pid else [None]:
            color_name = None
            color_img = None
            if v is not None:
                v_color_id = v.get("id_color")
                for name, cid in color_to_id.items():
                    if cid == v_color_id:
                        color_name = name
                        break
                color_img_row = next((cc for cc in colores_lista if cc.get("id_color") == v_color_id), None)
                color_img = color_img_row.get("img_color") if color_img_row else None
                image_row = next((im for im in imgs_pid if im.get("id_color") == v_color_id), None)
            else:
                image_row = imgs_pid[0] if imgs_pid else None

            filas.append({
                "id_producto": id_producto,
                "nombre_producto": base_p.get("nombre"),
                "precio": base_p.get("precio"),
                "descripcion": base_p.get("descripcion"),
                "id_categoria": cats_pid[0] if cats_pid else None,
                "nombre_categoria": cat_map.get(cats_pid[0]) if cats_pid else None,
                "id_variante": v.get("id_variante") if v else None,
                "id_talla": v.get("id_talla") if v else None,
                "color": color_name,
                "img_color": color_img,
                "talla": t_map.get(v.get("id_talla")) if v else None,
                "imagen_url": image_row.get("imagen_url") if image_row else None,
                "seccion": None,
            })
    base = filas[0]
    producto = {
        "id_producto": base.get("id_producto"),
        "nombre": base.get("nombre_producto", ""),
        "precio": base.get("precio", 0),
        "descripcion": base.get("descripcion", ""),
        "imagenes": [],
        "variantes": [],
        "categorias": [],
    }

    categorias_vistas = set()
    variantes_vistas = set()
    imagenes_vistas = set()
    for f in filas:
        img = f.get("imagen_url")
        if img and img not in imagenes_vistas:
            producto["imagenes"].append({"imagen_url": img, "id_color": color_to_id.get(f.get("color"))})
            imagenes_vistas.add(img)

        cid = f.get("id_categoria")
        if cid is not None and cid not in categorias_vistas:
            producto["categorias"].append({"id_categoria": cid, "nombre": f.get("nombre_categoria", "")})
            categorias_vistas.add(cid)

        vid = f.get("id_variante")
        id_talla = f.get("id_talla")
        if vid is not None and id_talla is not None and vid not in variantes_vistas:
            producto["variantes"].append(
                {
                    "id_variante": vid,
                    "color": {
                        "id_color": color_to_id.get(f.get("color")),
                        "color": f.get("color"),
                        "img_color": f.get("img_color"),
                    },
                    "talla": {
                        "id_talla": id_talla,
                        "talla": f.get("talla"),
                    },
                }
            )
            variantes_vistas.add(vid)

    if not producto["imagenes"]:
        producto["imagenes"] = [{"imagen_url": "/static/img/placeholder.jpg", "id_color": 0}]

    # --- Organizar imágenes por color
    imagenes_por_color = {}
    for imagen in producto.get("imagenes", []):
        color_id = imagen.get("id_color") or 0
        imagenes_por_color.setdefault(color_id, []).append(imagen.get("imagen_url"))

    # --- IDs de categorías del producto actual
    categorias_ids = [c.get("id_categoria") for c in producto.get("categorias", []) if c.get("id_categoria") is not None]

    # --- Productos recomendados: mismas categorías, excluyendo el actual
    productos_recomendados = []
    if categorias_ids:
        in_values = ",".join(str(x) for x in categorias_ids)
        filas_rec = select(
            "vista_productos_completa",
            {
                "select": "id_producto,nombre_producto,precio,id_variante,color,img_color,imagen_url,id_categoria",
                "id_categoria": f"in.({in_values})",
                "id_producto": f"neq.{id_producto}",
                "order": "id_producto.desc",
                "limit": "100",
            },
        )

        rec_map = {}
        for f in filas_rec:
            pid = f.get("id_producto")
            if pid is None:
                continue
            p = rec_map.get(pid)
            if not p:
                if len(rec_map) >= 4:
                    continue
                p = {
                    "id_producto": pid,
                    "nombre": f.get("nombre_producto", ""),
                    "precio": f.get("precio", 0),
                    "imagenes": [],
                    "variantes": [],
                }
                rec_map[pid] = p

            img = f.get("imagen_url")
            if img and not any(i.get("imagen_url") == img for i in p["imagenes"]):
                p["imagenes"].append({"imagen_url": img})

            vid = f.get("id_variante")
            cid = color_to_id.get(f.get("color"))
            if vid is not None and cid is not None and not any(v.get("id_variante") == vid for v in p["variantes"]):
                p["variantes"].append(
                    {
                        "id_variante": vid,
                        "color": {"id_color": cid, "img_color": f.get("img_color"), "color": f.get("color")},
                    }
                )

        productos_recomendados = list(rec_map.values())

    # --- Normalizar imágenes de productos recomendados
    for prod in productos_recomendados:
        valid_imgs = [img for img in prod.get("imagenes", []) if img.get("imagen_url")]
        if not valid_imgs:
            placeholder = {"imagen_url": "/static/img/placeholder.jpg"}
            prod["imagenes"] = [placeholder, placeholder]
        elif len(valid_imgs) == 1:
            prod["imagenes"] = [valid_imgs[0], valid_imgs[0]]
        else:
            prod["imagenes"] = valid_imgs

    # --- Buscar variante seleccionada si se envió POST
    id_variante = None
    id_color = request.form.get('id_color')
    id_talla = request.form.get('id_talla')
    if id_color and id_talla:
        variantes = select(
            "productos_variantes",
            {
                "select": "id_variante",
                "id_producto": f"eq.{id_producto}",
                "id_color": f"eq.{id_color}",
                "id_talla": f"eq.{id_talla}",
                "limit": "1",
            },
        )
        if variantes:
            id_variante = variantes[0].get("id_variante")

    return render_template(
        'productos/producto_detalle.html',
        producto=producto,
        imagenes_por_color=imagenes_por_color,
        productos=productos_recomendados,
        id_variante=id_variante
    )
