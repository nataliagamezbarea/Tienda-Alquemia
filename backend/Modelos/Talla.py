from backend.Modelos.database import db

class Talla(db.Model):
    __tablename__ = 'tallas'

    id_talla = db.Column(db.Integer, primary_key=True, autoincrement=True)
    talla = db.Column(db.String(10), unique=True, nullable=False)
