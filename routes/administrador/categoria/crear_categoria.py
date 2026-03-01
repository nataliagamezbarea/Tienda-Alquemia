from flask import render_template, request, redirect, url_for
from backend.supabase_rest import insert

def crear_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']

        insert("categorias", {"nombre": nombre})

        # Redirigir a la lista de categorías
        return redirect(url_for('listar_categorias'))
    
    return render_template('admin/categorias/crear_categoria.html')
