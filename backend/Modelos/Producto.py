from backend.Modelos.database import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    id_seccion = db.Column(db.Integer, db.ForeignKey('secciones.id_seccion'), nullable=False)  # Clave foránea a la tabla Secciones

    # Relaciones
    variantes = db.relationship('ProductoVariante', back_populates='producto')
    imagenes = db.relationship('ProductoImagen', back_populates='producto')

    seccion = db.relationship('Seccion', back_populates='productos')

    categorias = db.relationship('Categoria', secondary='producto_categoria', backref='productos')
