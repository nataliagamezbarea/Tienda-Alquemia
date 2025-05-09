import secrets
from itsdangerous import URLSafeTimedSerializer


# Clave secreta generada aleatoriamente al iniciar el servidor
clave_secreta = secrets.token_urlsafe(32)


def obtener_clave_secreta():
   return URLSafeTimedSerializer(clave_secreta)


