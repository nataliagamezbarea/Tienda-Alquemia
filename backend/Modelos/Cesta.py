from backend.Modelos.database import db
from backend.Modelos.CestaProducto import CestaProducto

class Cesta(db.Model):
    __tablename__ = 'cestas'

    id_cesta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # Relaciones
    productos = db.relationship('CestaProducto', backref='cestas', cascade="all, delete-orphan")
