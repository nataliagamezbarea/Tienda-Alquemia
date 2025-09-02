import os
import time
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()

db = SQLAlchemy()

def create_db_uri(user, password, host, port, database):
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def test_connection(uri, retries=5, delay=2):
    for _ in range(retries):
        try:
            engine = create_engine(uri)
            conn = engine.connect()
            conn.close()
            return True
        except OperationalError:
            time.sleep(delay)
    return False

def init_db(app):
    connections = []

    default_user = os.environ["DEFAULT_USER"]
    default_password = os.environ["DEFAULT_PASSWORD"]
    default_host = os.environ["DEFAULT_HOST"]
    default_port = os.environ["DEFAULT_PORT"]
    default_database = os.environ["DEFAULT_DATABASE"]

    connections.append({
        "USER": default_user,
        "PASSWORD": default_password,
        "HOST": default_host,
        "PORT": default_port,
        "DATABASE": default_database
    })

    i = 1
    while True:
        keys = [f"USER_{i}", f"PASSWORD_{i}", f"HOST_{i}", f"PORT_{i}", f"DATABASE_{i}"]
        if all(k in os.environ for k in keys):
            connections.append({
                "USER": os.environ[f"USER_{i}"],
                "PASSWORD": os.environ[f"PASSWORD_{i}"],
                "HOST": os.environ[f"HOST_{i}"],
                "PORT": os.environ[f"PORT_{i}"],
                "DATABASE": os.environ[f"DATABASE_{i}"],
            })
            i += 1
        else:
            break

    for conn in connections:
        uri = create_db_uri(
            conn["USER"],
            conn["PASSWORD"],
            conn["HOST"],
            conn["PORT"],
            conn["DATABASE"]
        )
        if test_connection(uri):
            app.config["SQLALCHEMY_DATABASE_URI"] = uri
            break
    else:
        raise Exception("No se pudo conectar a ninguna base de datos")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

# Inicializar Flask
app = Flask(__name__)
init_db(app)
