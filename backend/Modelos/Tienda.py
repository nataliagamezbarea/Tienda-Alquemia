from backend.Modelos.database import db 

class Tienda(db.Model):
    __tablename__ = 'tiendas'

    id_tienda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pais = db.Column(db.String(100)) 
    provincia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    maps_url = db.Column(db.String(500))   