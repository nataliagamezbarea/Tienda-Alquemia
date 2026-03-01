from flask import redirect, url_for, flash
from backend.supabase_rest import _request

def eliminar_producto(id_producto):
    _request("DELETE", "productos", params={"id_producto": f"eq.{id_producto}"})
    flash("Producto eliminado correctamente", "success")
    return redirect(url_for('productos'))
