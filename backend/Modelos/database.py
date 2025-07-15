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
    # Primero FreeSQLDatabase
    fs_user = os.getenv("FS_USER", "sql7790139")
    fs_password = os.getenv("FS_PASSWORD", "y4zICxtkL9")
    fs_host = os.getenv("FS_HOST", "sql7.freesqldatabase.com")
    fs_port = os.getenv("FS_PORT", "3306")
    fs_database = os.getenv("FS_DATABASE", "sql7790139")

    fs_uri = create_db_uri(fs_user, fs_password, fs_host, fs_port, fs_database)

    # Luego Clever Cloud
    cc_user = os.getenv("CC_USER", "ubqseyo86kiyzyti")
    cc_password = os.getenv("CC_PASSWORD", "P8l251fDC1VbceusYIp")
    cc_host = os.getenv("CC_HOST", "bvxjpato722w4r7ck9cc-mysql.services.clever-cloud.com")
    cc_port = os.getenv("CC_PORT", "21315")
    cc_database = os.getenv("CC_DATABASE", "bvxjpato722w4r7ck9cc")

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

# Ejemplo de uso con Flask
app = Flask(__name__)
init_db(app)
