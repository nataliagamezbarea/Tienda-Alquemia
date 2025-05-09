from flask import url_for
import random
from backend.Modelos import Categoria
from backend.Modelos.Producto import Producto
from backend.Modelos.ProductoCategoria import ProductoCategoria
from backend.Modelos.Seccion import Seccion

def obtener_menu(cache):
    # Función para obtener categorías de cache o BD
    def obtener_categorias(cache_key, filtro_seccion=None):
        categorias = cache.get(cache_key)
        if not categorias:
            query = Categoria.query
            if filtro_seccion:
                query = query.join(ProductoCategoria).join(Producto).join(Seccion).filter(Seccion.nombre == filtro_seccion)
            categorias = query.all()
            cache.set(cache_key, categorias, timeout=3600)
        return categorias

    # Función para obtener imágenes aleatorias de una sección
    def obtener_imagenes_random(seccion, cache_key):
        imagenes_random = cache.get(cache_key)
        if not imagenes_random:
            productos = Producto.query.join(Seccion).filter(Seccion.nombre == seccion).all()
            imagenes = [img.imagen_url for producto in productos for img in producto.imagenes if img.imagen_url]
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
