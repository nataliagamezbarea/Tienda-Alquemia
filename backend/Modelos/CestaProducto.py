from backend.Modelos.database import db

class CestaProducto(db.Model):
    __tablename__ = 'cestas_productos'

    id_cesta = db.Column(db.Integer, db.ForeignKey('cestas.id_cesta'), primary_key=True, nullable=False)
    id_variante = db.Column(db.Integer, db.ForeignKey('productos_variantes.id_variante'), primary_key=True, nullable=False)  
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    variante = db.relationship('ProductoVariante', backref='cestas_productos')