
from flask import Flask, render_template, request, redirect, url_for, session
from backend.supabase_rest import select, _request

def editar_devolucion(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    rows = select(
        "devoluciones",
        {"select": "id_devolucion,descripcion,hecha", "id_devolucion": f"eq.{id_devolucion}", "limit": "1"},
    )
    devolucion = rows[0] if rows else None
    if not devolucion:
        return "Devolución no encontrada", 404

    if request.method == 'POST':
        _request(
            "PATCH",
            "devoluciones",
            params={"id_devolucion": f"eq.{id_devolucion}"},
            payload={"descripcion": request.form['descripcion'], "hecha": 'hecha' in request.form},
        )
        return redirect(url_for('lista_devoluciones'))

    return render_template('admin/devoluciones/editar_devolucion.html', devolucion=devolucion)
