from backend.Modelos.database import db 

class PedidoTienda(db.Model):
    __tablename__ = 'pedido_tienda'

    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), primary_key=True, nullable=False)
    id_tienda = db.Column(db.Integer, db.ForeignKey('tiendas.id_tienda'), primary_key=True, nullable=False)


