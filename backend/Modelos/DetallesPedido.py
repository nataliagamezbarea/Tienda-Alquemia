from backend.Modelos.database import db 

class DetallesPedido(db.Model):
    __tablename__ = 'detalles_pedido'

    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), primary_key=True)
    tarjeta = db.Column(db.String(20), nullable=False)
    fecha_caducidad = db.Column(db.Date, nullable=False)
    csv = db.Column(db.String(4), nullable=False)
