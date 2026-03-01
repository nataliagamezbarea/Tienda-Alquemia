from flask import Flask, render_template, request, redirect, url_for, session
from backend.supabase_rest import _request


def eliminar_devolucion(id_devolucion):
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))

    _request("DELETE", "devoluciones", params={"id_devolucion": f"eq.{id_devolucion}"})
    return redirect(url_for('lista_devoluciones'))
