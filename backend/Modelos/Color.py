from backend.Modelos.database import db

class Color(db.Model):
    __tablename__ = 'colores'

    id_color = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), unique=True, nullable=False)
    img_color = db.Column(db.String(255))
