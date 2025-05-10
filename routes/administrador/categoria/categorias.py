from backend.Modelos import Categoria
from flask import render_template


def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('admin/categorias/lista_categorias.html', categorias=categorias)
