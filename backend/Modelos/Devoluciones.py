from backend.Modelos.database import db 

class Devoluciones(db.Model):
    __tablename__ = 'devoluciones'

    id_devolucion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), unique=True, nullable=False)
