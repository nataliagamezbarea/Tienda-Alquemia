from backend.Modelos.database import db

class Devoluciones(db.Model):
    __tablename__ = 'devoluciones'

    id_devolucion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text)
    hecha = db.Column(db.Boolean, default=False)  # Nuevo campo para marcar si la devolución fue hecha
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), unique=True, nullable=False)
    id_tienda = db.Column(db.Integer, db.ForeignKey('tiendas.id_tienda'), nullable=False)  # Relación con la tienda

    # Relación con la tabla 'Pedido'
    pedido = db.relationship('Pedido', backref=db.backref('devoluciones', lazy=True))
    
    # Relación con la tabla 'Tienda'
    tienda = db.relationship('Tienda', backref=db.backref('devoluciones', lazy=True))

    # Relación con 'ProductoVariante' a través de la tabla intermedia 'devoluciones_productos'
    productos = db.relationship('ProductoVariante', secondary='devoluciones_productos', backref=db.backref('devoluciones', lazy=True))
