from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import os

from backend.Modelos import (
    Producto, ProductoVariante, ProductoCategoria, ProductoImagen,
    Talla, Color, Seccion, Categoria
)
from backend.Modelos.database import db

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

        try:
            # Crear producto
            producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, id_seccion=id_seccion)
            db.session.add(producto)
            db.session.commit()

            # Asociar categorías
            for id_categoria in id_categorias:
                prod_cat = ProductoCategoria(id_producto=producto.id_producto, id_categoria=id_categoria)
                db.session.add(prod_cat)

            # Procesar variantes e imágenes
            i = 0
            while True:
                id_color = request.form.get(f'variantes[{i}][id_color]')
                id_talla = request.form.get(f'variantes[{i}][id_talla]')
                stock = request.form.get(f'variantes[{i}][stock]')

                if not id_color or not id_talla or not stock:
                    break

                # Crear variante
                producto_variante = ProductoVariante(
                    id_producto=producto.id_producto,
                    id_color=id_color,
                    id_talla=id_talla,
                    stock=stock
                )
                db.session.add(producto_variante)
                db.session.commit()

                # Obtener imágenes específicas de esta variante
                imagenes = request.files.getlist(f'variantes[{i}][imagenes][]')
                for imagen in imagenes:
                    ruta = guardar_imagen(imagen)
                    if ruta:
                        prod_img = ProductoImagen(
                            id_producto=producto.id_producto,
                            id_color=id_color,  # Asociar por color o producto_variante.id_variante si usas eso
                            imagen_url=ruta
                        )
                        db.session.add(prod_img)

                i += 1  # siguiente variante

            db.session.commit()

            flash("Producto creado exitosamente", "success")
            return redirect(url_for('productos'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error en la base de datos: {str(e)}", 'error')
            return redirect(url_for('productos'))

    # GET
    tallas = Talla.query.all()
    colores = Color.query.all()
    secciones = Seccion.query.all()
    categorias = Categoria.query.all()
    return render_template(
        'admin/agregar_producto.html',
        tallas=tallas, colores=colores, secciones=secciones, categorias=categorias
    )
