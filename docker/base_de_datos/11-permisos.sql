-- Script de permisos para PostgREST y PostgreSQL
-- Ejecutado automáticamente después de crear el schema

-- Dar permisos al usuario postgres sobre el schema
GRANT USAGE ON SCHEMA tienda_alquemia TO postgres;
GRANT CREATE ON SCHEMA tienda_alquemia TO postgres;

-- Dar SELECT en todas las tablas existentes
GRANT SELECT ON ALL TABLES IN SCHEMA tienda_alquemia TO postgres;

-- Dar SELECT en todas las vistas existentes
GRANT SELECT ON ALL TABLES IN SCHEMA tienda_alquemia TO postgres;

-- Permisos por defecto para tablas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA tienda_alquemia GRANT SELECT ON TABLES TO postgres;

-- Dar INSERT, UPDATE, DELETE en tablas específicas si es necesario
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA tienda_alquemia TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA tienda_alquemia GRANT INSERT, UPDATE, DELETE ON TABLES TO postgres;

-- Dar permisos en secuencias para auto-increment
GRANT USAGE ON ALL SEQUENCES IN SCHEMA tienda_alquemia TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA tienda_alquemia GRANT USAGE ON SEQUENCES TO postgres;
