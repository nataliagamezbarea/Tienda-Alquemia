-- Script de inicialización para PostgreSQL con Tienda Alquemia
-- Este archivo se ejecuta automáticamente al iniciar PostgreSQL

-- Crear schema tienda_alquemia si no existe
CREATE SCHEMA IF NOT EXISTS tienda_alquemia;

-- Dar permisos al usuario postgres sobre el schema
GRANT USAGE ON SCHEMA tienda_alquemia TO postgres;
GRANT CREATE ON SCHEMA tienda_alquemia TO postgres;

-- Establecer el search_path por defecto
ALTER ROLE postgres SET search_path = tienda_alquemia, public;

-- Hacer que tienda_alquemia sea el schema por defecto para nuevas tablas
SET search_path = tienda_alquemia, public;
