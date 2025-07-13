from flask_sqlalchemy import SQLAlchemy

# Creamos la instancia de la base de datos
db = SQLAlchemy()

# Datos del servidor MySQL para la base de datos remota
USER = "ubqseyo86kiyzyti"
PASSWORD = "P8l251fDC1VbceusYIp"
HOST = "bvxjpato722w4r7ck9cc-mysql.services.clever-cloud.com"
PORT = "21315"
DATABASE = "bvxjpato722w4r7ck9cc"

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
