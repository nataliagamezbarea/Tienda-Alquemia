from flask import Flask, render_template, request, redirect, url_for, session
from backend.Modelos.Devoluciones_Tiendas import DevolucionesTiendas
from backend.Modelos.database import db
from backend.Modelos.Devoluciones import Devoluciones




def obtener_devolucion(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    devolucion = Devoluciones.query.get(id_devolucion)
    if not devolucion:
        return "Devolución no encontrada", 404

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)
