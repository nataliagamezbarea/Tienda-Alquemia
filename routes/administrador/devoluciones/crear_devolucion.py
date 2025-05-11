from flask import Flask, render_template, request, redirect, url_for, session
from backend.Modelos.Devoluciones_Tiendas import DevolucionesTiendas
from backend.Modelos.database import db
from backend.Modelos.Devoluciones import Devoluciones

def crear_devolucion():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        id_pedido = request.form['id_pedido']
        id_variante = request.form['id_variante']

        nueva_devolucion = Devoluciones(
            descripcion=descripcion,
            id_pedido=id_pedido,
            id_variante=id_variante,
            hecha=False
        )

        db.session.add(nueva_devolucion)
        db.session.commit()

        return redirect(url_for('lista_devoluciones'))

    return render_template('admin/devoluciones/crear_devolucion.html')
