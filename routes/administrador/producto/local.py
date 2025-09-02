# backend/utils.py
import os
from flask import request

def es_local():
    """
    Detecta si la aplicación se está ejecutando en localhost.
    """
    default_host = os.getenv("DEFAULT_HOST", "127.0.0.1")
    current_host = request.host.split(":")[0]
    return default_host == current_host
