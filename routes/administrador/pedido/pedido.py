from flask import render_template, request, redirect, session, url_for, flash
from backend.Modelos.Pedido import Pedido
from backend.Modelos.database import db

def pedido():
    if "user" not in session or not session.get("is_admin"):
        return redirect(url_for("login"))
    if request.method == 'POST':
        pedido_id = request.form.get('pedido_id')
        nuevo_estado = request.form.get('estado')


        # Recupera el pedido de la base de datos
        pedido = Pedido.query.get(pedido_id)
        
        if pedido:
            # Verifica si el estado ya es el mismo
            if pedido.estado != nuevo_estado:
                pedido.estado = nuevo_estado
                db.session.commit()  # Guarda los cambios en la base de datos

                flash('El estado del pedido ha sido actualizado con éxito.', 'success')
            else:
                flash('El estado del pedido ya está actualizado.', 'info')
        else:
            flash('No se encontró el pedido.', 'error')

        return redirect(url_for('pedido'))  # Redirige para refrescar la página

    pedidos = Pedido.query.all()  # Obtiene todos los pedidos para mostrarlos
    return render_template('admin/pedidos/lista_pedidos.html', pedidos=pedidos)
