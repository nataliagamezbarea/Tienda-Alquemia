from backend.Modelos.database import db

class DevolucionesTiendas(db.Model):
    __tablename__ = 'devoluciones_tiendas'

    id_devolucion = db.Column(db.Integer, db.ForeignKey('devoluciones.id_devolucion'), primary_key=True)
    id_tienda = db.Column(db.Integer, db.ForeignKey('tiendas.id_tienda'), primary_key=True)

    devolucion = db.relationship(
        'Devoluciones',
        back_populates='devoluciones_tiendas',
        overlaps="devolucion, devoluciones_tiendas"
    )

    tienda = db.relationship(
        'Tienda',
        back_populates='devoluciones_tiendas',
        overlaps="tienda, devoluciones_tiendas"
    )
