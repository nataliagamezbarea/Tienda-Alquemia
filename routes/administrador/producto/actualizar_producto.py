from flask import flash, redirect, render_template, request, url_for
from backend.supabase_rest import select, insert, _request
from werkzeug.utils import secure_filename
import os
import time
from routes.administrador.producto.local import es_local  # función para localhost

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def actualizar_producto(producto_id):
    producto_rows = select(
        "productos",
        {"select": "id_producto,nombre,descripcion,precio,id_seccion", "id_producto": f"eq.{producto_id}", "limit": "1"},
    )
    if not producto_rows:
        flash("Producto no encontrado", "error")
        return redirect(url_for('productos'))
    producto = producto_rows[0]

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_seccion = request.form['id_seccion']
        id_categorias = request.form.getlist('id_categoria')

        if not id_seccion or not id_categorias:
            flash("Sección y categorías son obligatorias", "error")
            return redirect(request.url)

        _request(
            "PATCH",
            "productos",
            params={"id_producto": f"eq.{producto_id}"},
            payload={"nombre": nombre, "descripcion": descripcion, "precio": precio, "id_seccion": id_seccion},
        )

        # Actualizar categorías
        _request("DELETE", "productos_categorias", params={"id_producto": f"eq.{producto_id}"})
        rels = [{"id_producto": producto_id, "id_categoria": int(id_cat)} for id_cat in id_categorias]
        if rels:
            insert("productos_categorias", rels)

        # Reemplazar variantes e imágenes
        _request("DELETE", "productos_variantes", params={"id_producto": f"eq.{producto_id}"})
        _request("DELETE", "productos_imagenes_colores", params={"id_producto": f"eq.{producto_id}"})

        i = 0
        while True:
            id_color = request.form.get(f'variantes[{i}][id_color]')
            id_talla = request.form.get(f'variantes[{i}][id_talla]')
            stock = request.form.get(f'variantes[{i}][stock]')
            if not id_color or not id_talla or not stock:
                break

            insert(
                "productos_variantes",
                {
                    "id_producto": int(producto_id),
                    "id_color": int(id_color),
                    "id_talla": int(id_talla),
                    "stock": int(stock),
                },
            )

            # URLs (siempre se permiten)
            urls = request.form.getlist(f'variantes[{i}][imagen_url][]')
            for url in urls:
                url = (url or "").strip()
                if url:
                    insert(
                        "productos_imagenes_colores",
                        {
                            "id_producto": int(producto_id),
                            "id_color": int(id_color),
                            "imagen_url": url,
                        },
                    )

            # Imágenes subidas (solo si es local)
            if es_local():
                imagenes_nuevas = request.files.getlist(f'variantes[{i}][imagenes_nuevas]')
                for imagen in imagenes_nuevas:
                    if imagen and allowed_file(imagen.filename):
                        filename = secure_filename(imagen.filename)
                        unique_name = f"{int(time.time())}_{filename}"
                        ruta = os.path.join(UPLOAD_FOLDER, unique_name)
                        os.makedirs(os.path.dirname(ruta), exist_ok=True)
                        imagen.save(ruta)
                        insert(
                            "productos_imagenes_colores",
                            {
                                "id_producto": int(producto_id),
                                "id_color": int(id_color),
                                "imagen_url": '/' + ruta,
                            },
                        )

            i += 1

        flash("Producto actualizado exitosamente", "success")
        return redirect(url_for('productos'))

    # GET: recuperar datos para el formulario
    tallas = select("tallas", {"select": "id_talla,talla", "order": "id_talla.asc"})
    colores = select("colores", {"select": "id_color,color", "order": "id_color.asc"})
    secciones = select("secciones", {"select": "id_seccion,nombre", "order": "id_seccion.asc"})
    categorias = select("categorias", {"select": "id_categoria,nombre", "order": "id_categoria.asc"})

    rels = select("productos_categorias", {"select": "id_categoria", "id_producto": f"eq.{producto_id}"})
    categorias_producto = [r.get("id_categoria") for r in rels]

    variantes = select(
        "productos_variantes",
        {"select": "id_variante,id_producto,id_color,id_talla,stock", "id_producto": f"eq.{producto_id}", "order": "id_variante.asc"},
    )
    imagenes = select(
        "productos_imagenes_colores",
        {"select": "id_producto,id_color,imagen_url", "id_producto": f"eq.{producto_id}"},
    )
    for variante in variantes:
        variante["imagenes"] = [
            {"imagen_url": i.get("imagen_url")}
            for i in imagenes
            if i.get("id_color") == variante.get("id_color")
        ]

    return render_template(
        'admin/productos/editar_producto.html',
        producto=producto,
        tallas=tallas,
        colores=colores,
        secciones=secciones,
        categorias=categorias,
        categorias_producto=categorias_producto,
        variantes=variantes,
        es_localhost=es_local()
    )