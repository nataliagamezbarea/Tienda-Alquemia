from flask import url_for
import random
from backend.supabase_rest import select

def obtener_menu(cache):
    # Función para obtener categorías de cache o API
    def obtener_categorias(cache_key, seccion=None):
        categorias = cache.get(cache_key)
        if not categorias:
            if not seccion:
                categorias = select("categorias", {"select": "id_categoria,nombre", "order": "nombre.asc"})
            else:
                categorias = select(
                    "vista_productos_completa",
                    {
                        "select": "id_categoria,nombre_categoria",
                        "seccion": f"eq.{seccion}",
                        "order": "nombre_categoria.asc",
                    },
                )
                unicas = {}
                for c in categorias:
                    key = c.get("id_categoria")
                    if key is not None and key not in unicas:
                        unicas[key] = {"id_categoria": key, "nombre": c.get("nombre_categoria", "")}
                categorias = list(unicas.values())

            cache.set(cache_key, categorias, timeout=3600)
        return categorias

    # Función para obtener imágenes por sección desde la vista
    def obtener_imagenes_random(seccion, cache_key):
        imagenes_random = cache.get(cache_key)
        if not imagenes_random:
            filas = select(
                "vista_productos_completa",
                {
                    "select": "imagen_url",
                    "seccion": f"eq.{seccion}",
                    "order": "id_producto.desc",
                    "limit": "60",
                },
            )

            imagenes = [f.get("imagen_url") for f in filas if f.get("imagen_url")]
            imagenes_random = random.sample(imagenes, min(len(imagenes), 9)) if imagenes else []
            cache.set(cache_key, imagenes_random, timeout=3600)
        return imagenes_random

    # Obtener categorías y secciones aleatorias
    categorias = obtener_categorias('categorias')
    categorias_hombre = obtener_categorias('categorias_hombre', 'hombre')
    categorias_mujer = obtener_categorias('categorias_mujer', 'mujer')

    return {
        'categorias': categorias,
        'categorias_hombre': categorias_hombre,
        'categorias_mujer': categorias_mujer,
        'categorias_mujer_random': random.sample(categorias_mujer, min(len(categorias_mujer), 3)),
        'categorias_hombre_random': random.sample(categorias_hombre, min(len(categorias_hombre), 3)),
        'imagenes_mujer_random': obtener_imagenes_random('mujer', 'imagenes_mujer_random'),
        'imagenes_hombre_random': obtener_imagenes_random('hombre', 'imagenes_hombre_random'),
    }
