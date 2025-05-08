from backend.Modelos.database import db
from backend.Modelos.Color import Color
from backend.Modelos.Talla import Talla

class ProductoVariante(db.Model):
    __tablename__ = 'productos_variantes'

    id_variante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_color = db.Column(db.Integer, db.ForeignKey('colores.id_color'), nullable=False)
    id_talla = db.Column(db.Integer, db.ForeignKey('tallas.id_talla'), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='variantes')
    color = db.relationship('Color', backref='variantes')
    talla = db.relationship('Talla', backref='variantes')
