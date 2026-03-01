from flask import redirect, url_for, flash
from backend.supabase_rest import _request

def eliminar_categoria(categoria_id):
    _request("DELETE", "categorias", params={"id_categoria": f"eq.{categoria_id}"})

    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('listar_categorias'))
