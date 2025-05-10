from flask import render_template, request, redirect, url_for
from backend.Modelos.database import db
from backend.Modelos import Categoria

def crear_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']

        # Crear una nueva categoría
        nueva_categoria = Categoria(nombre=nombre)

        # Guardar en la base de datos
        db.session.add(nueva_categoria)
        db.session.commit()

        # Redirigir a la lista de categorías
        return redirect(url_for('listar_categorias'))
    
    return render_template('admin/categorias/crear_categoria.html')
