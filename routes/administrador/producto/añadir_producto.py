from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os

from backend.supabase_rest import select, insert
from routes.administrador.producto.local import es_local  # Función que detecta localhost

# Verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Guardar imagen y devolver ruta relativa
def guardar_imagen(imagen):
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        imagen.save(filepath)
        return f'/static/uploads/{filename}'
    return None

def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_seccion = request.form['id_seccion']
        id_categorias = request.form.getlist('id_categoria')

        if not id_seccion:
            flash("Error: Sección es obligatoria.", "error")
            return redirect(request.url)

        if not id_categorias:
            flash("Error: Se deben seleccionar al menos una categoría.", "error")
            return redirect(request.url)

        creado = insert(
            "productos",
            {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "id_seccion": id_seccion,
            },
        )
        if not creado:
            flash("Error al crear el producto", "error")
            return redirect(url_for('productos'))

        producto = creado[0]
        id_producto = producto.get("id_producto")

        # Asociar categorías
        rels = [{"id_producto": id_producto, "id_categoria": int(id_categoria)} for id_categoria in id_categorias]
        if rels:
            insert("productos_categorias", rels)

        # Procesar variantes
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
                    "id_producto": id_producto,
                    "id_color": int(id_color),
                    "id_talla": int(id_talla),
                    "stock": int(stock),
                },
            )

            # Guardar imágenes desde URLs dinámicas
            for key in request.form:
                if key.startswith(f'variantes[{i}][imagen_url]'):
                    url = request.form[key].strip()
                    if url:
                        insert(
                            "productos_imagenes_colores",
                            {
                                "id_producto": id_producto,
                                "id_color": int(id_color),
                                "imagen_url": url,
                            },
                        )

            # Guardar imágenes subidas
            imagenes = request.files.getlist(f'variantes[{i}][imagenes][]')
            for imagen in imagenes:
                ruta = guardar_imagen(imagen)
                if ruta:
                    insert(
                        "productos_imagenes_colores",
                        {
                            "id_producto": id_producto,
                            "id_color": int(id_color),
                            "imagen_url": ruta,
                        },
                    )

            i += 1

        flash("Producto creado exitosamente", "success")
        return redirect(url_for('productos'))

    # GET
    tallas = select("tallas", {"select": "id_talla,talla", "order": "id_talla.asc"})
    colores = select("colores", {"select": "id_color,color", "order": "id_color.asc"})
    secciones = select("secciones", {"select": "id_seccion,nombre", "order": "id_seccion.asc"})
    categorias = select("categorias", {"select": "id_categoria,nombre", "order": "id_categoria.asc"})

    return render_template(
        'admin/productos/agregar_producto.html',
        tallas=tallas,
        colores=colores,
        secciones=secciones,
        categorias=categorias,
        es_localhost=es_local()
    )
