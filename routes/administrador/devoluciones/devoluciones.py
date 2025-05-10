from flask import Flask, render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos.Devoluciones import Devoluciones  # Asegúrate de que este modelo esté importado correctamente


# Crear una nueva devolución
def crear_devolucion_view():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        id_pedido = request.form['id_pedido']
        id_variante = request.form['id_variante']

        # Crear una nueva devolución
        nueva_devolucion = Devoluciones(
            descripcion=descripcion,
            id_pedido=id_pedido,
            id_variante=id_variante,
            hecha=False  # Por defecto no está hecha
        )
        
        # Guardar en la base de datos
        db.session.add(nueva_devolucion)
        db.session.commit()

        return redirect(url_for('lista_devoluciones'))

    return render_template('crear_devolucion.html')


# Leer todas las devoluciones
def lista_devoluciones_view():
    devoluciones = Devoluciones.query.all()  # Obtiene todas las devoluciones
    return render_template('admin/devoluciones/lista_devoluciones.html', devoluciones=devoluciones)


# Leer una devolución específica por ID
def obtener_devolucion_view(id_devolucion):
    devolucion = Devoluciones.query.get(id_devolucion)
    if devolucion is None:
        return "Devolución no encontrada", 404

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)


# Actualizar una devolución
def editar_devolucion_view(id_devolucion):
    devolucion = Devoluciones.query.get(id_devolucion)
    if devolucion is None:
        return "Devolución no encontrada", 404

    if request.method == 'POST':
        devolucion.descripcion = request.form['descripcion']
        devolucion.hecha = 'hecha' in request.form

        db.session.commit()
        return redirect(url_for('lista_devoluciones'))

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)


# Eliminar una devolución
def eliminar_devolucion_view(id_devolucion):
    devolucion = Devoluciones.query.get(id_devolucion)
    if devolucion is None:
        return "Devolución no encontrada", 404

    db.session.delete(devolucion)
    db.session.commit()
    
    return redirect(url_for('lista_devoluciones'))

