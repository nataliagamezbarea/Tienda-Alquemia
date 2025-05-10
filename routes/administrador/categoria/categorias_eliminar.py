from backend.Modelos import Categoria
from backend.Modelos.database import db
from flask import redirect, url_for, flash

def eliminar_categoria(categoria_id):
    # Obtener la categoría por ID
    categoria = Categoria.query.get_or_404(categoria_id)

    # Eliminar las relaciones entre la categoría y los productos
    for producto in categoria.productos:
        categoria.productos.remove(producto)

    db.session.commit()  # Confirmamos la eliminación de las relaciones

    # Ahora eliminamos la categoría
    db.session.delete(categoria)
    db.session.commit()  # Confirmamos la eliminación de la categoría

    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('listar_categorias'))
