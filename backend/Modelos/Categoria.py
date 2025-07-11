from backend.Modelos.database import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    productos = db.relationship(
        'Producto',
        secondary='productos_categorias',
        back_populates='categorias',
        overlaps="productos_relacionados,categorias_relacionadas"
    )
