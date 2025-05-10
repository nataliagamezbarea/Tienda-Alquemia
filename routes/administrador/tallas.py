from flask import Flask, render_template, request, redirect, url_for, jsonify
from backend.Modelos.ProductoVariante import ProductoVariante
from backend.Modelos.database import db
from backend.Modelos.Talla import Talla


# LISTAR TODAS LAS TALLAS
def listar_tallas():
    tallas = Talla.query.all()
    return render_template('admin/talla/listar_tallas.html', tallas=tallas)

# CREAR UNA NUEVA TALLA
def crear_talla():
    if request.method == 'POST':
        talla = request.form.get('talla')
        
        if not talla:
            return jsonify({"error": "La talla es requerida"}), 400
        
        # Verificar si ya existe
        if Talla.query.filter_by(talla=talla).first():
            return jsonify({"error": "La talla ya existe"}), 400

        nueva_talla = Talla(talla=talla)
        db.session.add(nueva_talla)
        db.session.commit()

        return redirect(url_for('listar_tallas'))

    return render_template('crear_talla.html')

# EDITAR UNA TALLA
def editar_talla(id):
    talla = Talla.query.get_or_404(id)

    if request.method == 'POST':
        nueva_talla = request.form.get('talla')
        
        if not nueva_talla:
            return jsonify({"error": "La talla es requerida"}), 400

        # Verificar si el nuevo valor ya existe en otra fila
        existe = Talla.query.filter(Talla.talla == nueva_talla, Talla.id_talla != id).first()
        if existe:
            return jsonify({"error": "Ya existe otra talla con ese valor"}), 400

        talla.talla = nueva_talla
        db.session.commit()

        return redirect(url_for('listar_tallas'))

    return render_template('admin/talla/editar_talla.html', talla=talla)

def eliminar_talla(id):
    talla = Talla.query.get_or_404(id)

    try:
        # Eliminar las dependencias en producto_variantes
        producto_variantes = ProductoVariante.query.filter_by(id_talla=id).all()
        for pv in producto_variantes:
            db.session.delete(pv)

        # Eliminar la talla
        db.session.delete(talla)
        db.session.commit()
        return redirect(url_for('listar_tallas'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
