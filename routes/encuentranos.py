from flask import render_template
from backend.supabase_rest import select

def encuentranos():
    # Obtener todas las tiendas desde Supabase
    tiendas = select("tiendas", {
        "select": "id_tienda,pais,provincia,ciudad,codigo_postal,maps_url"
    })
    
    print(f"[DEBUG encuentranos] Tiendas recibidas: {len(tiendas) if isinstance(tiendas, list) else 'No es lista'}")
    print(f"[DEBUG encuentranos] Tipo de tiendas: {type(tiendas)}")
    
    if not isinstance(tiendas, list):
        tiendas = []

    # Obtener valores únicos para los filtros, ordenados
    paises = sorted(list(set([t.get("pais") for t in tiendas if t.get("pais")])))
    provincias = sorted(list(set([t.get("provincia") for t in tiendas if t.get("provincia")])))
    ciudades = sorted(list(set([t.get("ciudad") for t in tiendas if t.get("ciudad")])))

    print(f"[DEBUG encuentranos] Paises: {paises}")
    print(f"[DEBUG encuentranos] Provincias: {provincias}")
    print(f"[DEBUG encuentranos] Ciudades: {ciudades}")

    # Pasar los datos a la plantilla
    return render_template(
        'encuentranos.html',
        paises=paises,
        provincias=provincias,
        ciudades=ciudades,
        tiendas=tiendas
    )