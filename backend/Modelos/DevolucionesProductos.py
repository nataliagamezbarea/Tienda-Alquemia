from .database import db

class DevolucionesProducto(db.Model):
    __tablename__ = 'devoluciones_productos'
    id_devolucion = db.Column(db.Integer, db.ForeignKey('devoluciones.id_devolucion', ondelete='CASCADE'), primary_key=True)
    id_producto_variante = db.Column(db.Integer, db.ForeignKey('producto_variantes.id_variantes', ondelete='CASCADE'), primary_key=True)