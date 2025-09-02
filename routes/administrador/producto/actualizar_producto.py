from flask import flash, redirect, render_template, request, url_for
from backend.Modelos.ProductoVariante import ProductoVariante
from backend.Modelos.Talla import Talla
from backend.Modelos.database import db
from backend.Modelos import Categoria, Color, Producto, ProductoCategoria, ProductoImagen, Seccion
from werkzeug.utils import secure_filename
import os
import time
from sqlalchemy.exc import SQLAlchemyError
from routes.administrador.producto.local import es_local  # función para localhost

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def actualizar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_seccion = request.form['id_seccion']
        id_categorias = request.form.getlist('id_categoria')

        if not id_seccion or not id_categorias:
            flash("Sección y categorías son obligatorias", "error")
            return redirect(request.url)

        try:
            # Actualizar datos del producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.id_seccion = id_seccion
            db.session.commit()

            # Actualizar categorías
            ProductoCategoria.query.filter_by(id_producto=producto.id_producto).delete()
            for id_cat in id_categorias:
                db.session.add(ProductoCategoria(id_producto=producto.id_producto, id_categoria=id_cat))
            db.session.commit()

            # Eliminar variantes e imágenes anteriores
            ProductoVariante.query.filter_by(id_producto=producto.id_producto).delete()
            ProductoImagen.query.filter_by(id_producto=producto.id_producto).delete()
            db.session.commit()

            # Procesar variantes
            i = 0
            while True:
                id_color = request.form.get(f'variantes[{i}][id_color]')
                id_talla = request.form.get(f'variantes[{i}][id_talla]')
                stock = request.form.get(f'variantes[{i}][stock]')
                if not id_color or not id_talla or not stock:
                    break

                variante = ProductoVariante(id_producto=producto.id_producto, id_color=id_color, id_talla=id_talla, stock=stock)
                db.session.add(variante)
                db.session.commit()

                # URLs (siempre se permiten)
                urls = request.form.getlist(f'variantes[{i}][imagen_url][]')
                for url in urls:
                    if url:
                        db.session.add(ProductoImagen(id_producto=producto.id_producto, id_color=id_color, imagen_url=url))

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
                            # Guardar la ruta como url relativo para usar en frontend
                            db.session.add(ProductoImagen(id_producto=producto.id_producto, id_color=id_color, imagen_url='/' + ruta))

                i += 1

            db.session.commit()
            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for('productos'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error en la base de datos: {str(e)}", 'error')
            return redirect(url_for('productos'))

    # GET: recuperar datos para el formulario
    tallas = Talla.query.all()
    colores = Color.query.all()
    secciones = Seccion.query.all()
    categorias = Categoria.query.all()
    categorias_producto = [pc.id_categoria for pc in producto.categorias]
    variantes = ProductoVariante.query.filter_by(id_producto=producto.id_producto).all()
    for variante in variantes:
        variante.imagenes = ProductoImagen.query.filter_by(id_producto=producto.id_producto, id_color=variante.id_color).all()

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