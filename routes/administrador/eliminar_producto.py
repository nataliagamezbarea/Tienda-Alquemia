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
            return f"Error: Producto con id {id_producto} no encontrado."

        ProductoCategoria.query.filter_by(id_producto=id_producto).delete()
        ProductoVariante.query.filter_by(id_producto=id_producto).delete()
        ProductoImagen.query.filter_by(id_producto=id_producto).delete()
        db.session.delete(producto)
        db.session.commit()

        flash("Producto eliminado correctamente", "success")
        return redirect(url_for('productos'))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error en la base de datos: {str(e)}", 'error')
        return redirect(url_for('productos'))
