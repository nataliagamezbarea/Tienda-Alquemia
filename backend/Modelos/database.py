from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os

db = SQLAlchemy()

def create_db_uri(user, password, host, port, database):
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def test_connection(uri):
    try:
        engine = create_engine(uri)
        conn = engine.connect()
        conn.close()
        return True
    except OperationalError:
        return False

def init_db(app):
    # Obtener variables de entorno sin valores por defecto
    fs_user = os.environ["FS_USER"]
    fs_password = os.environ["FS_PASSWORD"]
    fs_host = os.environ["FS_HOST"]
    fs_port = os.environ["FS_PORT"]
    fs_database = os.environ["FS_DATABASE"]

    fs_uri = create_db_uri(fs_user, fs_password, fs_host, fs_port, fs_database)

    cc_user = os.environ["CC_USER"]
    cc_password = os.environ["CC_PASSWORD"]
    cc_host = os.environ["CC_HOST"]
    cc_port = os.environ["CC_PORT"]
    cc_database = os.environ["CC_DATABASE"]

    cc_uri = create_db_uri(cc_user, cc_password, cc_host, cc_port, cc_database)

    if test_connection(fs_uri):
        app.config["SQLALCHEMY_DATABASE_URI"] = fs_uri
        print("Conectado a FreeSQLDatabase")
    elif test_connection(cc_uri):
        app.config["SQLALCHEMY_DATABASE_URI"] = cc_uri
        print("Conectado a Clever Cloud")
    else:
        raise Exception("No se pudo conectar a ninguna base de datos")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

# Uso en una app Flask
app = Flask(__name__)
init_db(app)
