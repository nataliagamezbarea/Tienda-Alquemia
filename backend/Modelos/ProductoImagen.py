from backend.Modelos.database import db

class ProductoImagen(db.Model):
    __tablename__ = 'producto_imagenes'

    id_imagen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_color = db.Column(db.Integer, db.ForeignKey('colores.id_color'), nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='imagenes')
