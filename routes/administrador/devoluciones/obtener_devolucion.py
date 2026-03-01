from flask import Flask, render_template, request, redirect, url_for, session
from backend.supabase_rest import select




def obtener_devolucion(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    rows = select(
        "devoluciones",
        {"select": "id_devolucion,descripcion,hecha", "id_devolucion": f"eq.{id_devolucion}", "limit": "1"},
    )
    devolucion = rows[0] if rows else None
    if not devolucion:
        return "Devolución no encontrada", 404

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)
