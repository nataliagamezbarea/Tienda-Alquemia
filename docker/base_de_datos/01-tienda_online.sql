-- Crear esquema tienda_alquemia
CREATE SCHEMA IF NOT EXISTS tienda_alquemia;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS tienda_alquemia.usuarios (
    id_usuario     SERIAL PRIMARY KEY,
    nombre         VARCHAR(50) NOT NULL,
    apellido1      VARCHAR(50) NOT NULL,
    apellido2      VARCHAR(50),
    email          VARCHAR(100) NOT NULL UNIQUE,
    contrasena     VARCHAR(100) NOT NULL,
    is_admin       BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabla de colores
CREATE TABLE IF NOT EXISTS tienda_alquemia.colores (
    id_color       SERIAL PRIMARY KEY,
    color          VARCHAR(50) NOT NULL UNIQUE,
    img_color      VARCHAR(255) NOT NULL
);

-- Tabla de tallas
CREATE TABLE IF NOT EXISTS tienda_alquemia.tallas (
    id_talla       SERIAL PRIMARY KEY,
    talla          VARCHAR(10) NOT NULL UNIQUE
);

-- Tabla de secciones
CREATE TABLE IF NOT EXISTS tienda_alquemia.secciones (
    id_seccion     SERIAL PRIMARY KEY,
    nombre         VARCHAR(20) NOT NULL CHECK (nombre IN ('hombre', 'mujer', 'niño', 'niña', 'unisex'))
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS tienda_alquemia.categorias (
    id_categoria   SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL
);

-- Tabla de tiendas
CREATE TABLE IF NOT EXISTS tienda_alquemia.tiendas (
    id_tienda      SERIAL PRIMARY KEY,
    provincia      VARCHAR(100) NOT NULL,
    ciudad         VARCHAR(100) NOT NULL,
    codigo_postal  VARCHAR(10) NOT NULL, 
    pais           VARCHAR(100) NOT NULL, 
    maps_url       TEXT NOT NULL
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS tienda_alquemia.productos (
    id_producto    SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    id_seccion     INT NOT NULL,
    precio         DECIMAL(10,2) NOT NULL,
    descripcion    TEXT NOT NULL,
    FOREIGN KEY (id_seccion) REFERENCES tienda_alquemia.secciones(id_seccion) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tienda_alquemia.productos_imagenes_colores (
    id_imagen      SERIAL PRIMARY KEY,
    id_producto    INT NOT NULL,
    id_color       INT NOT NULL,
    imagen_url     VARCHAR(255) NOT NULL,
    UNIQUE (id_producto, id_color, imagen_url),
    FOREIGN KEY (id_producto) REFERENCES tienda_alquemia.productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_color) REFERENCES tienda_alquemia.colores(id_color) ON DELETE CASCADE
);

-- Tabla de variantes de productos
CREATE TABLE IF NOT EXISTS tienda_alquemia.productos_variantes (
    id_variante    SERIAL PRIMARY KEY,
    id_producto    INT NOT NULL,
    id_color       INT NOT NULL,
    id_talla       INT NOT NULL,
    stock          INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    UNIQUE (id_producto, id_color, id_talla),
    FOREIGN KEY (id_producto) REFERENCES tienda_alquemia.productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_color) REFERENCES tienda_alquemia.colores(id_color) ON DELETE CASCADE,
    FOREIGN KEY (id_talla) REFERENCES tienda_alquemia.tallas(id_talla) ON DELETE CASCADE
);

-- Tabla de relación producto-categoría
CREATE TABLE IF NOT EXISTS tienda_alquemia.productos_categorias (
    id_producto    INT NOT NULL,
    id_categoria   INT NOT NULL,
    PRIMARY KEY (id_producto, id_categoria),
    FOREIGN KEY (id_producto) REFERENCES tienda_alquemia.productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES tienda_alquemia.categorias(id_categoria) ON DELETE CASCADE
);

-- Tabla de cestas
CREATE TABLE IF NOT EXISTS tienda_alquemia.cestas (
    id_cesta       SERIAL PRIMARY KEY,
    id_usuario     INT NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES tienda_alquemia.usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de productos en la cesta
CREATE TABLE IF NOT EXISTS tienda_alquemia.cestas_productos (
    id_cesta       INT NOT NULL,
    id_variante    INT NOT NULL,
    cantidad       INT NOT NULL DEFAULT 1 CHECK (cantidad > 0),
    PRIMARY KEY (id_cesta, id_variante),
    FOREIGN KEY (id_cesta) REFERENCES tienda_alquemia.cestas(id_cesta) ON DELETE CASCADE,
    FOREIGN KEY (id_variante) REFERENCES tienda_alquemia.productos_variantes(id_variante) ON DELETE CASCADE
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS tienda_alquemia.pedidos (
    id_pedido SERIAL PRIMARY KEY,
    nombre_envio VARCHAR(100) NOT NULL,
    apellido1_envio VARCHAR(50) NOT NULL,
    apellido2_envio VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado')),
    tipo_pedido VARCHAR(20) NOT NULL DEFAULT 'domicilio' CHECK (tipo_pedido IN ('domicilio', 'tienda')),
    fecha DATE NOT NULL,
    id_usuario INT NOT NULL,
    id_tienda INT NULL,
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES tienda_alquemia.usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_tienda) REFERENCES tienda_alquemia.tiendas(id_tienda)
);

-- Tabla de productos en el pedido
CREATE TABLE IF NOT EXISTS tienda_alquemia.pedidos_productos (
    id_pedido       INT NOT NULL,
    id_variante     INT NOT NULL,
    cantidad        INT NOT NULL DEFAULT 1 CHECK (cantidad > 0),
    total_producto  DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (id_pedido, id_variante),
    FOREIGN KEY (id_pedido) REFERENCES tienda_alquemia.pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_variante) REFERENCES tienda_alquemia.productos_variantes(id_variante) ON DELETE CASCADE
);

-- Tabla de devoluciones
CREATE TABLE IF NOT EXISTS tienda_alquemia.devoluciones (
    id_devolucion     SERIAL PRIMARY KEY,
    descripcion       TEXT NOT NULL,
    id_pedido         INT NOT NULL,
    id_variante       INT NOT NULL,
    fecha_devolucion  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hecha             BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_pedido, id_variante) 
        REFERENCES tienda_alquemia.pedidos_productos(id_pedido, id_variante) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tienda_alquemia.devoluciones_tiendas (
    id_devolucion INT NOT NULL,
    id_tienda     INT NOT NULL,
    PRIMARY KEY (id_devolucion, id_tienda),
    FOREIGN KEY (id_devolucion) REFERENCES tienda_alquemia.devoluciones(id_devolucion) ON DELETE CASCADE,
    FOREIGN KEY (id_tienda) REFERENCES tienda_alquemia.tiendas(id_tienda) ON DELETE CASCADE
);

-- Vista de productos completos
DROP VIEW IF EXISTS tienda_alquemia.vista_productos_completa;
CREATE VIEW tienda_alquemia.vista_productos_completa AS
SELECT 
    p.id_producto,
    p.nombre AS nombre_producto,
    p.precio,
    p.descripcion,
    s.nombre AS seccion,
    c.id_categoria,
    c.nombre AS nombre_categoria,
    v.id_variante,
    v.stock,
    col.color,
    col.img_color,
    t.talla,
    pic.imagen_url
FROM tienda_alquemia.productos p
JOIN tienda_alquemia.secciones s ON p.id_seccion = s.id_seccion
JOIN tienda_alquemia.productos_variantes v ON v.id_producto = p.id_producto
JOIN tienda_alquemia.colores col ON v.id_color = col.id_color
JOIN tienda_alquemia.tallas t ON v.id_talla = t.id_talla
JOIN tienda_alquemia.productos_categorias pc ON p.id_producto = pc.id_producto
JOIN tienda_alquemia.categorias c ON pc.id_categoria = c.id_categoria
JOIN tienda_alquemia.productos_imagenes_colores pic ON pic.id_producto = p.id_producto AND pic.id_color = col.id_color;

-- Función para actualizar stock después de un pedido (PostgreSQL)
CREATE OR REPLACE FUNCTION tienda_alquemia.actualizar_stock_despues_compra()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE tienda_alquemia.productos_variantes
    SET stock = stock - NEW.cantidad
    WHERE id_variante = NEW.id_variante;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para la función
DROP TRIGGER IF EXISTS actualizar_stock_despues_compra ON tienda_alquemia.pedidos_productos;
CREATE TRIGGER actualizar_stock_despues_compra
AFTER INSERT ON tienda_alquemia.pedidos_productos
FOR EACH ROW
EXECUTE FUNCTION tienda_alquemia.actualizar_stock_despues_compra();
