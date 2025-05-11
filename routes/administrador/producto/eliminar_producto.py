from flask import redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from backend.Modelos import (
    Producto, ProductoVariante, ProductoCategoria, ProductoImagen
)
from backend.Modelos.database import db


def eliminar_producto(id_producto):
    try:
        producto = Producto.query.get(id_producto)
        if not producto:
            flash(f"Error: Producto con id {id_producto} no encontrado.", "error")
            return redirect(url_for('productos'))

        # Eliminar las relaciones manualmente
        for variante in producto.variantes:
            db.session.delete(variante)
        
        for imagen in producto.imagenes:
            db.session.delete(imagen)
        
        for categoria in producto.categorias:
            # Aquí no eliminamos las categorías, solo la relación
            producto.categorias.remove(categoria)

        # Eliminar el producto
        db.session.delete(producto)
        db.session.commit()

        flash("Producto eliminado correctamente", "success")
        return redirect(url_for('productos'))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error en la base de datos: {str(e)}", 'error')
        return redirect(url_for('productos'))
