from flask import render_template, session
from backend.Modelos.database import db
from backend.Modelos.CestaProducto import CestaProducto
from backend.Modelos.Cesta import Cesta
from backend.Modelos.ProductoImagen import ProductoImagen
from backend.Modelos.ProductoVariante import ProductoVariante

def home():
    return render_template(
        "home.html",
       
    )
