from flask import Flask, render_template, request, redirect, url_for, flash
from backend.Modelos import Categoria  # Importa el modelo de Categoria
from backend.Modelos.database import db  # Importa el objeto db

def editar_categoria(categoria_id):
    # Obtener la categoría a editar
    categoria = Categoria.query.get_or_404(categoria_id)
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        categoria.nombre = request.form['nombre']
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('listar_categorias'))  # Redirige a la lista de categorías
    
    return render_template('admin/categorias/editar_categoria.html', categoria=categoria)
