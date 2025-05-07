from backend.Modelos.database import db

class Seccion(db.Model):
    __tablename__ = 'secciones'

    id_seccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Enum('hombre', 'mujer', 'niño', 'niña', 'unisex'), nullable=False)

    # Relación con la tabla Producto (uno a muchos)
    productos = db.relationship('Producto', back_populates='seccion')
