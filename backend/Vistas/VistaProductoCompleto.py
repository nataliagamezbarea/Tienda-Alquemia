from backend.Modelos.database import db

class VistaProductoCompleto(db.Model):
    __tablename__ = 'vista_productos_completa'
    __table_args__ = {'extend_existing': True}  # opcional

    id_variante = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer)
    nombre_producto = db.Column(db.String)  # Nombre del producto
    precio = db.Column(db.Numeric(10, 2))  # Precio del producto
    descripcion = db.Column(db.Text)  # Descripción del producto
    seccion = db.Column(db.String)  # Nombre de la sección
    id_categoria = db.Column(db.Integer)  # ID de la categoría
    nombre_categoria = db.Column(db.String)  # Nombre de la categoría
    stock = db.Column(db.Integer)  # Stock del producto
    color = db.Column(db.String)  # Color del producto
    img_color = db.Column(db.String)  # Imagen del color del producto
    talla = db.Column(db.String)  # Talla del producto
    imagen_url = db.Column(db.String)  # URL de la imagen del producto

