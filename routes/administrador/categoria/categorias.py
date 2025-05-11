from flask import render_template, session, redirect, url_for
from backend.Modelos import Categoria

def listar_categorias():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for('login'))  
    
    categorias = Categoria.query.all()
    return render_template('admin/categorias/lista_categorias.html', categorias=categorias)
