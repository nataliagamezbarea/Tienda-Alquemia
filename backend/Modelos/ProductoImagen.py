from backend.Modelos.database import db

class ProductoImagen(db.Model):
    __tablename__ = 'productos_imagenes_colores'

    # Definir la clave primaria compuesta por id_producto e id_color
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), primary_key=True, nullable=False)
    id_color = db.Column(db.Integer, db.ForeignKey('colores.id_color'), primary_key=True, nullable=False)
    
    # Columna para almacenar la URL de la imagen
    imagen_url = db.Column(db.String(255), nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='imagenes')
    color = db.relationship('Color', back_populates='imagenes')
