from flask import Flask, render_template, request, redirect, url_for, flash
from backend.supabase_rest import select, _request

def editar_categoria(categoria_id):
    # Obtener la categoría a editar
    rows = select("categorias", {"select": "id_categoria,nombre", "id_categoria": f"eq.{categoria_id}", "limit": "1"})
    if not rows:
        return "Categoría no encontrada", 404
    categoria = rows[0]
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        
        # Guardar los cambios en la base de datos
        _request("PATCH", "categorias", params={"id_categoria": f"eq.{categoria_id}"}, payload={"nombre": nombre})
        
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('listar_categorias'))  # Redirige a la lista de categorías
    
    return render_template('admin/categorias/editar_categoria.html', categoria=categoria)
