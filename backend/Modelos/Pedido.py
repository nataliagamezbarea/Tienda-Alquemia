from backend.Modelos.database import db
from sqlalchemy.orm import relationship

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_envio = db.Column(db.String(100), nullable=False)
    apellido1_envio = db.Column(db.String(50), nullable=False)
    apellido2_envio = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50))
    tipo_pedido = db.Column(db.String(50))
    fecha = db.Column(db.Date, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    pedido_productos = relationship('PedidoProducto', backref='pedidos_productos', lazy=True)
    
