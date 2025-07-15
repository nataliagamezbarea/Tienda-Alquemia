import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

db = SQLAlchemy()

def create_db_uri(user, password, host, port, database):
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def test_connection(uri):
    try:
        engine = create_engine(uri)
        conn = engine.connect()
        conn.close()
        return True
    except OperationalError as e:
        print(f"Error al conectar con la URI {uri}: {e}")
        return False

def init_db(app):
    # Freesqldatabase
    fs_user = os.getenv("FS_USER")
    fs_password = os.getenv("FS_PASSWORD")
    fs_host = os.getenv("FS_HOST")
    fs_port = os.getenv("FS_PORT")
    fs_database = os.getenv("FS_DATABASE")

    # Clever Cloud
    cc_user = os.getenv("CC_USER")
    cc_password = os.getenv("CC_PASSWORD")
    cc_host = os.getenv("CC_HOST")
    cc_port = os.getenv("CC_PORT")
    cc_database = os.getenv("CC_DATABASE")

    # Validar que existan
    if not fs_user or not fs_password or not fs_host or not fs_port or not fs_database:
        print("⚠️ Variables FS_* faltan o no se cargaron desde el archivo .env")
    if not cc_user or not cc_password or not cc_host or not cc_port or not cc_database:
        print("⚠️ Variables CC_* faltan o no se cargaron desde el archivo .env")

    fs_uri = create_db_uri(fs_user, fs_password, fs_host, fs_port, fs_database)
    cc_uri = create_db_uri(cc_user, cc_password, cc_host, cc_port, cc_database)

    # Probar conexión
    if test_connection(fs_uri):
        print("✅ Conexión exitosa con FreeSQLDatabase")
        app.config["SQLALCHEMY_DATABASE_URI"] = fs_uri
    elif test_connection(cc_uri):
        print("✅ Conexión exitosa con Clever Cloud")
        app.config["SQLALCHEMY_DATABASE_URI"] = cc_uri
    else:
        raise Exception("❌ No se pudo conectar a ninguna base de datos")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
