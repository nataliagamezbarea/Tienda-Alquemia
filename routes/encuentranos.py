from flask import render_template
from backend.Modelos.database import db
from backend.Modelos.Tienda import Tienda

def encuentranos():
    # Obtener todos los países, provincias y ciudades disponibles en la base de datos
    paises = db.session.query(Tienda.pais).distinct().all()
    provincias = db.session.query(Tienda.provincia).distinct().all()
    ciudades = db.session.query(Tienda.ciudad).distinct().all()

    # Obtener todas las tiendas sin aplicar filtros
    tiendas = Tienda.query.all()

    # Pasar los datos a la plantilla
    return render_template(
        'encuentranos.html',
        paises=paises,
        provincias=provincias,
        ciudades=ciudades,
        tiendas=tiendas
    )
