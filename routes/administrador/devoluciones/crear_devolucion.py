from flask import Flask, render_template, request, redirect, url_for, session
from backend.supabase_rest import insert

def crear_devolucion():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        id_pedido = request.form['id_pedido']
        id_variante = request.form['id_variante']

        insert(
            "devoluciones",
            {
                "descripcion": descripcion,
                "id_pedido": int(id_pedido),
                "id_variante": int(id_variante),
                "hecha": False,
            },
        )

        return redirect(url_for('lista_devoluciones'))

    return redirect(url_for('lista_devoluciones'))
