from backend.Modelos.database import db

class CestaProducto(db.Model):
    __tablename__ = 'cesta_productos'

    id_cesta = db.Column(db.Integer, db.ForeignKey('cesta.id_cesta'), primary_key=True, nullable=False)
    id_variantes = db.Column(db.Integer, db.ForeignKey('producto_variantes.id'), primary_key=True, nullable=False)  
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    id_cesta = db.Column(db.Integer, db.ForeignKey('cesta.id_cesta'), primary_key=True, nullable=False)
    id_variantes = db.Column(db.Integer, db.ForeignKey('producto_variantes.id_variantes'), primary_key=True, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    variante = db.relationship('ProductoVariante', backref='cesta_productos')