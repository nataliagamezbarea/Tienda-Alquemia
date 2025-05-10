from flask import flash, redirect, render_template, request, url_for
from backend.Modelos.ProductoVariante import ProductoVariante
from backend.Modelos.Talla import Talla
from backend.Modelos.database import db
from backend.Modelos import Categoria, Color, Producto, ProductoCategoria, ProductoImagen, Seccion
from werkzeug.utils import secure_filename
import os
import time
from sqlalchemy.exc import SQLAlchemyError

# Definir el directorio para guardar las imágenes
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def actualizar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_seccion = request.form['id_seccion']
        id_categorias = request.form.getlist('id_categoria')

        # Validaciones
        if not id_seccion:
            flash("Error: Sección es obligatoria.", "error")
            return redirect(request.url)

        if not id_categorias:
            flash("Error: Se deben seleccionar al menos una categoría.", "error")
            return redirect(request.url)

        try:
            # Actualizar el producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.id_seccion = id_seccion
            db.session.commit()

            # Actualizar categorías
            ProductoCategoria.query.filter_by(id_producto=producto.id_producto).delete()
            for id_categoria in id_categorias:
                db.session.add(ProductoCategoria(id_producto=producto.id_producto, id_categoria=id_categoria))

            # Eliminar variantes y sus imágenes anteriores
            ProductoVariante.query.filter_by(id_producto=producto.id_producto).delete()
            ProductoImagen.query.filter_by(id_producto=producto.id_producto).delete()

            # Procesar variantes y asociar imágenes
            i = 0
            while True:
                id_color = request.form.get(f'variantes[{i}][id_color]')
                id_talla = request.form.get(f'variantes[{i}][id_talla]')
                stock = request.form.get(f'variantes[{i}][stock]')
                if not id_color or not id_talla or not stock:
                    break

                # Crear nueva variante
                nueva_variante = ProductoVariante(id_producto=producto.id_producto, id_color=id_color, id_talla=id_talla, stock=stock)
                db.session.add(nueva_variante)
                db.session.commit()

                # Obtener imágenes existentes y nuevas
                imagenes_existentes = request.form.get(f'variantes[{i}][imagenes_existentes]')
                imagenes_nuevas = request.files.getlist(f'variantes[{i}][imagenes_nuevas]')

                # Procesar imágenes existentes
                if imagenes_existentes:
                    imagenes_existentes = imagenes_existentes.split(',')
                    for imagen_url in imagenes_existentes:
                        db.session.add(ProductoImagen(id_producto=producto.id_producto, id_color=id_color, imagen_url=imagen_url))

                # Subir nuevas imágenes
                for imagen in imagenes_nuevas:
                    if imagen and allowed_file(imagen.filename):
                        filename = secure_filename(imagen.filename)
                        timestamp = str(int(time.time()))
                        unique_filename = f"{timestamp}_{filename}"
                        ruta = os.path.join(UPLOAD_FOLDER, unique_filename)
                        imagen.save(ruta)

                        # Guardar la ruta de la nueva imagen
                        db.session.add(ProductoImagen(id_producto=producto.id_producto, id_color=id_color, imagen_url=ruta))

                db.session.commit()
                i += 1

            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for('productos'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error en la base de datos: {str(e)}", 'error')
            return redirect(url_for('productos'))

    # GET: Recuperar las imágenes de las variantes
    tallas = Talla.query.all()
    colores = Color.query.all()
    secciones = Seccion.query.all()
    categorias = Categoria.query.all()
    categorias_producto = [pc.id_categoria for pc in producto.categorias]
    variantes = ProductoVariante.query.filter_by(id_producto=producto.id_producto).all()

    for variante in variantes:
        # Obtener imágenes para cada variante
        variante.imagenes = ProductoImagen.query.filter_by(id_producto=producto.id_producto, id_color=variante.id_color).all()

    return render_template(
        'admin/editar_producto.html',
        producto=producto,
        tallas=tallas,
        colores=colores,
        secciones=secciones, 
        categorias=categorias, 
        categorias_producto=categorias_producto,
        variantes=variantes
    )
