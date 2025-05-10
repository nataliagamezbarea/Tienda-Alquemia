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

# Crear producto
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        id_categoria = request.form['id_categoria']
        id_seccion = request.form['id_seccion']

        if not id_seccion:
            return "Error: Sección es obligatoria."

        try:
            producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, id_seccion=id_seccion)
            db.session.add(producto)
            db.session.commit()

            # Procesar variantes
            variantes = request.form.getlist('variantes')
            for variante in variantes:
                id_color = variante['id_color']
                id_talla = variante['id_talla']
                stock = variante['stock']
                producto_variante = ProductoVariante(
                    id_producto=producto.id_producto,
                    id_color=id_color,
                    id_talla=id_talla,
                    stock=stock
                )
                db.session.add(producto_variante)

            # Asociar categorías
            prod_cat = ProductoCategoria(id_producto=producto.id_producto, id_categoria=id_categoria)
            db.session.add(prod_cat)

            db.session.commit()

            # Manejar imágenes
            if 'imagenes' in request.files:
                imagenes = request.files.getlist('imagenes')
                for imagen in imagenes:
                    ruta = guardar_imagen(imagen)
                    if ruta:
                        for variante in variantes:
                            prod_img = ProductoImagen(
                                id_producto=producto.id_producto,
                                id_color=variante['id_color'],
                                imagen_url=ruta
                            )
                            db.session.add(prod_img)

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
    return render_template('admin/agregar_producto.html', tallas=tallas, colores=colores, secciones=secciones, categorias=categorias)

# Eliminar producto
def eliminar_producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        if not producto:
            return f"Error: Producto con id {id_producto} no encontrado."

        ProductoCategoria.query.filter_by(id_producto=id_producto).delete()
        ProductoVariante.query.filter_by(id_producto=id_producto).delete()
        ProductoImagen.query.filter_by(id_producto=id_producto).delete()
        db.session.delete(producto)
        db.session.commit()

        flash("Producto eliminado correctamente", "success")
        return redirect(url_for('productos'))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error en la base de datos: {str(e)}", 'error')
        return redirect(url_for('productos'))

# Obtener productos y renderizar HTML
def obtener_productos_html():
    productos = Producto.query.all()
    productos_dict = {}

    for producto in productos:
        pid = producto.id_producto
        productos_dict[pid] = {
            'id_producto': pid,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'variantes': [],
            'imagenes': [],
            'categorias': ', '.join([c.nombre for c in producto.categorias]),
            'colores': set(),
            'tallas': set(),
            'secciones': producto.seccion.nombre if producto.seccion else '',
            'stock_total': 0,
        }

        for variante in producto.variantes:
            productos_dict[pid]['variantes'].append({
                'color': variante.color.color,
                'talla': variante.talla.talla,
                'stock': variante.stock
            })
            productos_dict[pid]['colores'].add(variante.color.color)
            productos_dict[pid]['tallas'].add(variante.talla.talla)
            productos_dict[pid]['stock_total'] += variante.stock

        for imagen in producto.imagenes:
            productos_dict[pid]['imagenes'].append({
                'imagen_url': imagen.imagen_url,
                'color': imagen.color.color
            })

        productos_dict[pid]['colores'] = ', '.join(productos_dict[pid]['colores'])
        productos_dict[pid]['tallas'] = ', '.join(productos_dict[pid]['tallas'])

    productos_ordenados = sorted(productos_dict.values(), key=lambda x: x['precio'], reverse=True)

    secciones = [(s.id_seccion, s.nombre) for s in Seccion.query.all()]
    colores = [(c.id_color, c.color) for c in Color.query.all()]
    tallas = [(t.id_talla, t.talla) for t in Talla.query.all()]
    categorias = [(c.id_categoria, c.nombre) for c in Categoria.query.all()]

    return render_template(
        'admin/productos.html',
        productos=productos_ordenados,
        secciones=secciones,
        colores=colores,
        tallas=tallas,
        categorias=categorias
    )
