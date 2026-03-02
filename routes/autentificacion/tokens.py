import os
from itsdangerous import URLSafeTimedSerializer


def obtener_clave_secreta():
    # Usar la SECRET_KEY del .env para que sea consistente entre instancias
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise ValueError("SECRET_KEY no está configurada en las variables de entorno")
    return URLSafeTimedSerializer(secret_key)


