USE tienda_alquemia;
SET NAMES 'utf8mb4';

INSERT INTO usuarios (nombre, apellido1, apellido2, email, contrasena, is_admin) VALUES
('Pedro', 'Lopez', 'Ruiz', 'pedro.lopez@example.com', '$2b$12$zeOTT1HubRNW5KsZQp97A.zlsL3RmPpj9l1Xc.Ww7Phpcejsesqru', FALSE),
('Laura', 'Pérez', NULL, 'laura.perez@example.com', '$2b$12$L0Wf.TXmTSpC2sYsOfQraOCAtZPFWRzColtlPcv3a2W2UGU9wkT0W', TRUE),
('Laura', 'García', 'Pérez', 'laura.garcia@example.com', '$2b$12$/oOrqw6bJeJJyGdg.pk9XOMVzLIFKoeb8/1pPxSmfm8yCye/820EO', FALSE),
('Laura', 'Martínez', 'Jiménez', 'laura.martinez@example.com', '$2b$12$5.Q/jNlKR0W4gdO.w.ITi.WLPPXR7V7SsldvKHpxLgNVf0hwtmnbK', FALSE),
('Maria', 'García', 'Jiménez', 'maria.garcia@example.com', '$2b$12$/t5YPRTnqDisA7uRKnL6Z.qUyABlcCnexze.L0GjlRIkSjgfFXLQK', FALSE),
('David', 'García', NULL, 'david.garcia@example.com', '$2b$12$RvgNbeRcpylzb70T1QI5l.t6AEaHacbzuux2k0peAel/Xlxpbf4Ku', FALSE),
('Marta', 'Pérez', NULL, 'marta.perez@example.com', '$2b$12$i9cet9RLcY3gMGFn8XewGuhC9Z5h35iKurdhRGChvIPcee5otWGnC', FALSE),
('Laura', 'Rodríguez', NULL, 'laura.rodriguez@example.com', '$2b$12$0uKKhAzqqbUM78BE/YSBruFwR.uZulvpYsZQ0n2KtNLqv3Ht/vzF6', FALSE),
('Laura', 'González', NULL, 'laura.gonzalez@example.com', '$2b$12$IkJoB9ZVt6F9ZZL/eki7dOa5.4uruW9Rx.6mWr7jM2HaeCz8qElG.', FALSE),
('Luis', 'González', 'Jiménez', 'luis.gonzalez@example.com', '$2b$12$KqpGEhQDDa9x5UmzY59QHeitlBzJ9FJczw5Xp7GJXM4Sj8Uf7nXIO', FALSE);


INSERT INTO cestas (id_usuario, fecha_creacion) VALUES
(1, NOW()),
(3, NOW()),
(4, NOW());



INSERT INTO cestas_productos (id_cesta, id_variante, cantidad) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 1),
(3, 4, 3);



INSERT INTO tiendas (provincia, ciudad, codigo_postal, pais, maps_url) VALUES
('Madrid', 'Alcalá de Henares', '28801', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d47913.07375897295!2d2.0369610397433657!3d41.361762006755974!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12a499201356d7e9%3A0x1053c8717c5ad841!2sVERDETT%20by%20Vero%20MODA!5e0!3m2!1ses!2ses!4v1746909043707!5m2!1ses!2ses'),
('Barcelona', 'L\'Hospitalet de Llobregat', '08901', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d24653.907260296975!2d-0.5129882228185438!3d39.43003946669003!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd60517840a2c36d%3A0x440424ee8ef35707!2sCalzedonia!5e0!3m2!1ses!2ses!4v1746909230092!5m2!1ses!2ses'),
('Valencia', 'Torrent', '46900', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6025.289303014734!2d-5.668432479662977!3d40.967362784947085!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd3f2611471aebc3%3A0xad3593ae9522a616!2sGloria%20Galende%20%7C%20Boutique%20de%20Moda%20Mujer%20en%20Salamanca!5e0!3m2!1ses!2ses!4v1746909294694!5m2!1ses!2ses'),
('Sevilla', 'Dos Hermanas', '41701', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d25581.82192786269!2d-4.450360592231741!3d36.72909946769293!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd72f796711e2801%3A0xa57db8a68a08e299!2sCENTROMODA%20M%C3%81LAGA!5e0!3m2!1ses!2ses!4v1746909361488!5m2!1ses!2ses'),
('Zaragoza', 'La Almunia de Doña Godina', '50400', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d25187.58946429355!2d-4.824321984375025!3d37.896574!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd6cdf2d2d3b21ed%3A0xfdce299a30c9a21e!2sTienda%20C%C3%B3rdoba%20CF!5e0!3m2!1ses!2ses!4v1746909403661!5m2!1ses!2ses'),
('Málaga', 'Ronda', '29400', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3018138.018163208!2d-9.801273099206!3d42.37661593983606!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd2f62629b4bd4b5%3A0x603f7ce058f1cb65!2sKabu!5e0!3m2!1ses!2ses!4v1746909441287!5m2!1ses!2ses'),
('Murcia', 'Cartagena', '30201', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23204.956180863344!2d-8.43061942705645!3d43.3640686437759!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd2e7c9b99c8a6d9%3A0x5e4cf3e2f9295b6f!2sBOSS%20Menswear%20Shop!5e0!3m2!1ses!2ses!4v1746909471494!5m2!1ses!2ses'),
('Palma', 'Calvià', '07180', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11927.425465905771!2d-4.756581492187506!3d41.63723599999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd476d3a3a21bd33%3A0xf6fe4e4e10e13e41!2sBOSS%20Menswear%20Shop!5e0!3m2!1ses!2ses!4v1746909488808!5m2!1ses!2ses'),
('Bilbao', 'Getxo', '48991', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23848.58986642291!2d-0.913277831164305!3d41.6541489034106!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd5914e61d2970c9%3A0xbb58faec25450324!2sIKKS%20Women!5e0!3m2!1ses!2ses!4v1746909507734!5m2!1ses!2ses'),
('Alicante', 'Elche', '03201', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d776840.6333520941!2d1.734200509599805!3d40.48557936548123!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12a4a292c3efafb1%3A0x4b8dabace9f58700!2sANJARA%20BARCELONA!5e0!3m2!1ses!2ses!4v1746909522599!5m2!1ses!2ses'),
('Córdoba', 'Pozoblanco', '14400', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11610.89741098114!2d-1.989416126958389!3d43.320029435988594!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd51a5166d3575f1%3A0x8a3e858158c1907f!2sCCHIKA%20-%20Tienda%20de%20moda%20Mujer%20.!5e0!3m2!1ses!2ses!4v1746909537531!5m2!1ses!2ses'),
('Valladolid', 'Medina del Campo', '47600', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23245.02092867513!2d-2.947023727312099!3d43.25922569417664!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd4e4f5b45000c45%3A0x1042ae479d578ed3!2sBlue%20Banana%20Brand%20-%20Bilbao!5e0!3m2!1ses!2ses!4v1746909556126!5m2!1ses!2ses'),
('Vigo', 'Ponteareas', '36860', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d50066.94442094879!2d-0.5550892687500126!3d38.34472249999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd62371c25357189%3A0xc7c0d02007f3131a!2sClassy%20Priv%C4%93e!5e0!3m2!1ses!2ses!4v1746909585091!5m2!1ses!2ses'),
('Gijón', 'Avilés', '33400', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d50066.954384631434!2d-0.5552609616184961!3d38.3447080853629!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd6236eb9f33cf81%3A0x930639a10f0ea743!2sDeportes%20Match!5e0!3m2!1ses!2ses!4v1746909604070!5m2!1ses!2ses'),
('Granada', 'Almuñécar', '18690', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6294482.534097686!2d-5.978224604528674!3d39.616444464022734!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd6a0ba5eb3822b1%3A0x2de91f90e87485c2!2sCoquette!5e0') , 
('San Sebastián', 'Irun', '20301', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23204.956180863344!2d-8.43061942705645!3d43.3640686437759!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd2e7c9b99c8a6d9%3A0x5e4cf3e2f9295b6f!2sBOSS%20Menswear%20Shop!5e0!3m2!1ses!2ses!4v1746909471494!5m2!1ses!2ses'),
('A Coruña', 'Oleiros', '15173', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d776840.6333520941!2d1.734200509599805!3d40.48557936548123!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12a4a292c3efafb1%3A0x4b8dabace9f58700!2sANJARA%20BARCELONA!5e0!3m2!1ses!2ses!4v1746909522599!5m2!1ses!2ses'),
('Toledo', 'Consuegra', '45700', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11927.425465905771!2d-4.756581492187506!3d41.63723599999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd476d3a3a21bd33%3A0xf6fe4e4e10e13e41!2sBOSS%20Menswear%20Shop!5e0!3m2!1ses!2ses!4v1746909488808!5m2!1ses!2ses'),
('Burgos', 'Aranda de Duero', '09400', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23245.02092867513!2d-2.947023727312099!3d43.25922569417664!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd4e4f5b45000c45%3A0x1042ae479d578ed3!2sBlue%20Banana%20Brand%20-%20Bilbao!5e0!3m2!1ses!2ses!4v1746909556126!5m2!1ses!2ses'),
('Salamanca', 'Santa Marta de Tormes', '37900', 'España', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12578.512433046151!2d-1.1442652921875331!3d37.985807400000006!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd63821afd1d4419%3A0xc23fd199d74d0ca0!2sWoman%20Boutique%20Tienda%20Ropa%20Mujer%20en%20Murcia!5e0!3m2!1ses!2ses!4v1746909667411!5m2!1ses!2ses');


INSERT INTO pedidos (nombre_envio, apellido1_envio, apellido2_envio, estado, tipo_pedido, fecha, id_usuario, id_tienda, entregado) VALUES
('Ana', 'García', 'López', 'procesando', 'domicilio', CURDATE(), 1, NULL, FALSE),
('Lucía', 'Martínez', 'Sánchez', 'enviado', 'tienda', CURDATE(), 3, 1, FALSE),
('Miguel', 'Ruiz', '', 'entregado', 'domicilio', CURDATE(), 4, NULL, TRUE),
('Pedro', 'Pérez', 'Gómez', 'procesando', 'tienda', CURDATE(), 2, 1, FALSE),
('Laura', 'Jiménez', 'Rodríguez', 'enviado', 'domicilio', CURDATE(), 5, NULL, FALSE),
('Juan', 'González', '', 'entregado', 'tienda', CURDATE(), 6, 2, TRUE),
('Carlos', 'Sánchez', 'Torres', 'procesando', 'domicilio', CURDATE(), 7, NULL, FALSE),
('María', 'López', 'García', 'enviado', 'tienda', CURDATE(), 8, 1, FALSE),
('Raúl', 'Martín', 'Hernández', 'entregado', 'domicilio', CURDATE(), 9, NULL, TRUE),
('Esther', 'Vázquez', 'Castro', 'procesando', 'tienda', CURDATE(), 10, 2, FALSE);


INSERT INTO pedidos_productos (id_pedido, id_variante, cantidad, total_producto) VALUES
(1, 1, 2, 39.98),     -- Pedido 1, Variante 1, 2 unidades, total 39.98
(1, 2, 1, 19.99),     -- Pedido 1, Variante 2, 1 unidad, total 19.99
(2, 3, 1, 24.99),     -- Pedido 2, Variante 3, 1 unidad, total 24.99
(2, 4, 2, 49.98),     -- Pedido 2, Variante 4, 2 unidades, total 49.98
(3, 5, 3, 59.97),     -- Pedido 3, Variante 5, 3 unidades, total 59.97
(3, 6, 1, 19.99),     -- Pedido 3, Variante 6, 1 unidad, total 19.99
(4, 7, 4, 79.96),     -- Pedido 4, Variante 7, 4 unidades, total 79.96
(4, 8, 2, 39.98),     -- Pedido 4, Variante 8, 2 unidades, total 39.98
(5, 1, 5, 99.90),     -- Pedido 5, Variante 1, 5 unidades, total 99.90
(5, 9, 3, 74.97),     -- Pedido 5, Variante 9, 3 unidades, total 74.97
(6, 10, 1, 24.99),    -- Pedido 6, Variante 10, 1 unidad, total 24.99
(6, 2, 2, 39.98),     -- Pedido 6, Variante 2, 2 unidades, total 39.98
(7, 3, 6, 149.94),    -- Pedido 7, Variante 3, 6 unidades, total 149.94
(7, 4, 1, 24.99),     -- Pedido 7, Variante 4, 1 unidad, total 24.99
(8, 5, 2, 39.98),     -- Pedido 8, Variante 5, 2 unidades, total 39.98
(8, 6, 3, 59.97),     -- Pedido 8, Variante 6, 3 unidades, total 59.97
(9, 7, 1, 19.99),     -- Pedido 9, Variante 7, 1 unidad, total 19.99
(9, 8, 4, 79.96),     -- Pedido 9, Variante 8, 4 unidades, total 79.96
(10, 9, 2, 49.98),    -- Pedido 10, Variante 9, 2 unidades, total 49.98
(10, 10, 1, 24.99);   -- Pedido 10, Variante 10, 1 unidad, total 24.99



INSERT INTO devoluciones (descripcion, id_pedido, id_variante) 
VALUES 
('Producto defectuoso', 1, 1),
('Cambio de talla', 1, 2),
('Producto dañado', 2, 3),
('Producto incorrecto', 2, 4),
('No me gusta', 3, 5),
('Producto defectuoso', 3, 6),
('Error en el pedido', 4, 7),
('Cambio de color', 4, 8),
('Producto no corresponde', 5, 1),
('Defecto de fabricación', 5, 9),
('No me interesa', 6, 10),
('Cambio por talla incorrecta', 6, 2),
('Producto dañado durante el envío', 7, 3),
('No es lo que esperaba', 7, 4),
('Producto defectuoso', 8, 5),
('Cambio por otra variante', 8, 6),
('Producto roto', 9, 7),
('Cambio de color solicitado', 9, 8),
('Producto defectuoso', 10, 9),
('No me gusta el producto', 10, 10);



INSERT INTO devoluciones_tiendas (id_devolucion, id_tienda) 
VALUES 
(1, 1),  -- Devolución 1, gestionada por la tienda con id_tienda 1 (Alcalá de Henares)
(2, 2),  -- Devolución 2, gestionada por la tienda con id_tienda 2 (L'Hospitalet de Llobregat)
(3, 3),  -- Devolución 3, gestionada por la tienda con id_tienda 3 (Torrent)
(4, 4),  -- Devolución 4, gestionada por la tienda con id_tienda 4 (Dos Hermanas)
(5, 5),  -- Devolución 5, gestionada por la tienda con id_tienda 5 (La Almunia de Doña Godina)
(6, 6),  -- Devolución 6, gestionada por la tienda con id_tienda 6 (Ronda)
(7, 7),  -- Devolución 7, gestionada por la tienda con id_tienda 7 (Cartagena)
(8, 8),  -- Devolución 8, gestionada por la tienda con id_tienda 8 (Calvià)
(9, 9),  -- Devolución 9, gestionada por la tienda con id_tienda 9 (Getxo)
(10, 10); -- Devolución 10, gestionada por la tienda con id_tienda 10 (Elche)
