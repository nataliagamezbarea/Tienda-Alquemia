from flask import render_template, request, redirect, url_for, flash
from backend.Modelos.Pedido import Pedido
from backend.Modelos.database import db

def pedido():
    if request.method == 'POST':
        pedido_id = request.form.get('pedido_id')
        nuevo_estado = request.form.get('estado')

        print(f"Pedido ID: {pedido_id}")  # Depuración: Verifica que el ID se recibe correctamente
        print(f"Nuevo estado: {nuevo_estado}")  # Depuración: Verifica que el estado se recibe correctamente

        # Recupera el pedido de la base de datos
        pedido = Pedido.query.get(pedido_id)
        
        if pedido:
            # Verifica si el estado ya es el mismo
            if pedido.estado != nuevo_estado:
                print(f"Estado antes de la actualización: {pedido.estado}")  # Depuración
                pedido.estado = nuevo_estado
                db.session.commit()  # Guarda los cambios en la base de datos
                print(f"Estado después de la actualización: {pedido.estado}")  # Depuración

                flash('El estado del pedido ha sido actualizado con éxito.', 'success')
            else:
                flash('El estado del pedido ya está actualizado.', 'info')
        else:
            flash('No se encontró el pedido.', 'error')

        return redirect(url_for('pedido'))  # Redirige para refrescar la página

    pedidos = Pedido.query.all()  # Obtiene todos los pedidos para mostrarlos
    return render_template('admin/pedidos/lista_pedidos.html', pedidos=pedidos)
