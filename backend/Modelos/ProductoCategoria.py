from backend.Modelos.database import db

class ProductoCategoria(db.Model):
    __tablename__ = 'producto_categoria'

    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), primary_key=True)
