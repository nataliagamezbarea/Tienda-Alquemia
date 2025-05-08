from backend.Modelos.database import db

class ProductoColor(db.Model):
    __tablename__ = 'producto_color'

    id_color_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colores.id_color'), nullable=False)
    img_producto = db.Column(db.Text, nullable=False)

    producto = db.relationship('Producto', backref='color_images')
    color = db.relationship('Color', backref='color_images')
