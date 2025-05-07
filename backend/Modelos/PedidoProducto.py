from backend.Modelos.database import db
from sqlalchemy.orm import relationship
from backend.Modelos.ProductoVariante import ProductoVariante
from backend.Modelos.Pedido import Pedido

class PedidoProducto(db.Model):
    __tablename__ = 'pedido_productos'

    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), primary_key=True)
    id_variantes = db.Column(db.Integer, db.ForeignKey('producto_variantes.id_variantes'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    total_producto = db.Column(db.Float, nullable=False, default=0.00)

    pedido = db.relationship('Pedido', backref='pedido_productos_rel', lazy=True)
    producto_variante = db.relationship('ProductoVariante', backref='pedido_productos')
