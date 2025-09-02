USE tienda_alquemia;
ALTER DATABASE tienda_alquemia CHARACTER SET utf8 COLLATE utf8_spanish2_ci;


-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario     INT PRIMARY KEY AUTO_INCREMENT,
    nombre         VARCHAR(50) NOT NULL,
    apellido1      VARCHAR(50) NOT NULL,
    apellido2      VARCHAR(50),
    email          VARCHAR(100) NOT NULL UNIQUE,
    contrasena     VARCHAR(100) NOT NULL,
    is_admin       BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabla de colores
CREATE TABLE colores (
    id_color       INT PRIMARY KEY AUTO_INCREMENT,
    color          VARCHAR(50) NOT NULL UNIQUE,
    img_color      VARCHAR(255) NOT NULL
);

-- Tabla de tallas
CREATE TABLE tallas (
    id_talla       INT PRIMARY KEY AUTO_INCREMENT,
    talla          VARCHAR(10) NOT NULL UNIQUE
);

-- Tabla de secciones
CREATE TABLE secciones (
    id_seccion     INT PRIMARY KEY AUTO_INCREMENT,
    nombre         ENUM('hombre', 'mujer', 'niño', 'niña', 'unisex') NOT NULL,
    CHECK (nombre IN ('hombre', 'mujer', 'niño', 'niña', 'unisex')) -- Restricción CHECK
);

-- Tabla de categorías
CREATE TABLE categorias (
    id_categoria   INT PRIMARY KEY AUTO_INCREMENT,
    nombre         VARCHAR(100) NOT NULL
);

-- Tabla de tiendas
CREATE TABLE tiendas (
    id_tienda      INT PRIMARY KEY AUTO_INCREMENT,
    provincia      VARCHAR(100) NOT NULL,
    ciudad         VARCHAR(100) NOT NULL,
    codigo_postal  VARCHAR(10) NOT NULL, 
    pais           VARCHAR(100) NOT NULL, 
    maps_url       TEXT NOT NULL
);

-- Tabla de productos
CREATE TABLE productos (
    id_producto    INT PRIMARY KEY AUTO_INCREMENT,
    nombre         VARCHAR(100) NOT NULL,
    id_seccion     INT NOT NULL,
    precio         DECIMAL(10,2) NOT NULL,
    descripcion    TEXT NOT NULL,
    FOREIGN KEY (id_seccion) REFERENCES secciones(id_seccion) ON DELETE CASCADE
);

CREATE TABLE productos_imagenes_colores (
    id_imagen      INT PRIMARY KEY AUTO_INCREMENT,
    id_producto    INT NOT NULL,
    id_color       INT NOT NULL,
    imagen_url     VARCHAR(255) NOT NULL,
    CONSTRAINT uq_producto_color_url UNIQUE (id_producto, id_color, imagen_url),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_color) REFERENCES colores(id_color) ON DELETE CASCADE
);

-- Tabla de variantes de productos
CREATE TABLE productos_variantes (
    id_variante   INT PRIMARY KEY AUTO_INCREMENT,
    id_producto    INT NOT NULL,
    id_color       INT NOT NULL,
    id_talla       INT NOT NULL,
    stock          INT NOT NULL DEFAULT 0 CHECK (stock >= 0), -- Restricción CHECK
    CONSTRAINT uq_producto_color_talla UNIQUE (id_producto, id_color, id_talla), -- Para que no se pueda insertar productos variantes iguales
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_color) REFERENCES colores(id_color) ON DELETE CASCADE,
    FOREIGN KEY (id_talla) REFERENCES tallas(id_talla) ON DELETE CASCADE
);

-- Tabla de relación producto-categoría
CREATE TABLE productos_categorias (
    id_producto    INT NOT NULL,
    id_categoria   INT NOT NULL,
    PRIMARY KEY (id_producto, id_categoria),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

-- Tabla de cestas
CREATE TABLE cestas (
    id_cesta       INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario     INT NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de productos en la cesta
CREATE TABLE cestas_productos (
    id_cesta       INT NOT NULL,
    id_variante    INT NOT NULL,
    cantidad       INT NOT NULL DEFAULT 1 CHECK (cantidad > 0), -- Restricción CHECK
    PRIMARY KEY (id_cesta, id_variante),
    FOREIGN KEY (id_cesta) REFERENCES cestas(id_cesta) ON DELETE CASCADE,
    FOREIGN KEY (id_variante) REFERENCES productos_variantes(id_variante) ON DELETE CASCADE
);

-- Tabla de pedidos
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,  -- Clave primaria
    nombre_envio VARCHAR(100) NOT NULL,
    apellido1_envio VARCHAR(50) NOT NULL,
    apellido2_envio VARCHAR(50) NOT NULL,
    estado ENUM('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado') NOT NULL DEFAULT 'pendiente',
    tipo_pedido ENUM('domicilio', 'tienda') NOT NULL DEFAULT 'domicilio',
    fecha DATE NOT NULL,
    id_usuario INT NOT NULL,
    id_tienda INT NULL,  -- Permitimos que sea NULL
    entregado BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id_tienda)
);

-- Tabla de productos en el pedido
CREATE TABLE pedidos_productos (
    id_pedido       INT NOT NULL,
    id_variante     INT NOT NULL,
    cantidad        INT NOT NULL DEFAULT 1 CHECK (cantidad > 0), -- Restricción CHECK
    total_producto  DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (id_pedido, id_variante),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_variante) REFERENCES productos_variantes(id_variante) ON DELETE CASCADE
);

-- Tabla de devoluciones
CREATE TABLE devoluciones (
    id_devolucion     INT PRIMARY KEY AUTO_INCREMENT,
    descripcion       TEXT NOT NULL,
    id_pedido         INT NOT NULL,
    id_variante       INT NOT NULL,
    fecha_devolucion  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hecha             BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_pedido, id_variante) 
        REFERENCES pedidos_productos(id_pedido, id_variante) 
        ON DELETE CASCADE
);

CREATE TABLE devoluciones_tiendas (
    id_devolucion INT NOT NULL,
    id_tienda     INT NOT NULL,
    PRIMARY KEY (id_devolucion, id_tienda),
    FOREIGN KEY (id_devolucion) REFERENCES devoluciones(id_devolucion) ON DELETE CASCADE,
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id_tienda) ON DELETE CASCADE
);

-- Vista de productos completos
CREATE VIEW vista_productos_completa AS
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
FROM productos p
JOIN secciones s ON p.id_seccion = s.id_seccion
JOIN productos_variantes v ON v.id_producto = p.id_producto
JOIN colores col ON v.id_color = col.id_color
JOIN tallas t ON v.id_talla = t.id_talla
JOIN productos_categorias pc ON p.id_producto = pc.id_producto
JOIN categorias c ON pc.id_categoria = c.id_categoria
JOIN productos_imagenes_colores pic ON pic.id_producto = p.id_producto AND pic.id_color = col.id_color;

DELIMITER $$

-- Trigger para actualizar stock después de un pedido
CREATE TRIGGER actualizar_stock_despues_compra
AFTER INSERT ON pedidos_productos
FOR EACH ROW
BEGIN
    UPDATE productos_variantes
    SET stock = stock - NEW.cantidad
    WHERE id_variante = NEW.id_variante;
END $$

DELIMITER ;
