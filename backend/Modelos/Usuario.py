from backend.Modelos.database import db 
from sqlalchemy.orm import relationship

class Usuario(db.Model): 
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido1 = db.Column(db.String(50), nullable=True)
    apellido2 = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    contrasena =  db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False , default = False)

    pedidos = relationship('Pedido', backref='usuario', lazy=True)
