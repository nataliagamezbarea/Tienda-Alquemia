from backend.Modelos.database import db

class DevolucionesTiendas(db.Model):
    __tablename__ = 'devoluciones_tiendas'

    id_devolucion = db.Column(db.Integer, db.ForeignKey('devoluciones.id_devolucion'), primary_key=True)
    id_tienda = db.Column(db.Integer, db.ForeignKey('tiendas.id_tienda'), primary_key=True)

    # Relación con el modelo 'Devoluciones'
    devolucion = db.relationship('Devoluciones', backref='devoluciones_tiendas_relacionadas', lazy=True)

    # Relación con el modelo 'Tienda'
    tienda = db.relationship('Tienda', backref='devoluciones_tienda_relacionadas', lazy=True)
