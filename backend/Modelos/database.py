import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def _build_database_url() -> str:
    # Conexión directa (sin pooler)
    database_url = os.getenv("DATABASE_URL", "").strip()

    if not database_url:
        raise ValueError("Falta DATABASE_URL en .env")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    if "sslmode=" not in database_url:
        joiner = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{joiner}sslmode=require"

    return database_url


def init_db(app):
    rest_only = os.getenv("SUPABASE_REST_ONLY", "true").lower() in ("1", "true", "yes")

    # Evita intentos de conexión directa PostgreSQL (IPv6) cuando trabajamos por REST
    if rest_only:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        return

    database_url = _build_database_url()

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "connect_args": {
            "options": "-csearch_path=tienda_alquemia,public",
            "connect_timeout": 8,
        }
    }

    db.init_app(app)


def get_db():
    return db
