from backend.Modelos.database import db

class Devoluciones(db.Model):
    __tablename__ = 'devoluciones'

    id_devolucion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text, nullable=False)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos_productos.id_pedido'), nullable=False)
    id_variante = db.Column(db.Integer, db.ForeignKey('pedidos_productos.id_variante'), nullable=False)
    fecha_devolucion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    hecha = db.Column(db.Boolean, default=False, nullable=False)

    devoluciones_tiendas = db.relationship(
        'DevolucionesTiendas',
        back_populates='devolucion',
        cascade="all, delete-orphan",
        overlaps="devolucion, devoluciones_tiendas"
    )