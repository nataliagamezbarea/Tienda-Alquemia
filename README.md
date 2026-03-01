# 🛍️ Tienda de Ropa - Alquemia

Bienvenido al repositorio de **Alquemia**, una aplicación web para la gestión de una tienda de ropa. Aquí puedes ver productos, gestionarlos y realizar compras desde una interfaz amigable y moderna.

---

## 🚀 Características

- Catálogo de ropa con fotos, precios y descripciones
- Carrito de compras funcional
- Panel de administración para agregar, editar y eliminar productos
- Autenticación de usuarios (particular y empresa)
- Gestión de pedidos y devoluciones
- Diseño responsivo para móviles y escritorio
- Envío de correos para registro, pedidos y contacto

---

## ⚙️ Instalación en local

### 1. Clona este repositorio

```bash
git clone https://github.com/nataliagamezbarea/Tienda-Alquemia
cd Tienda-Alquemia
```

### 2. Instala los requerimientos de Python

Se recomienda crear un entorno virtual antes de instalar dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configura el entorno

Copia el archivo `.env.example` a `.env` y rellena tus variables (o revisa que los valores por defecto sean válidos para desarrollo).

---

## 🐳 Ejecución con Docker Compose

Toda la infraestructura necesaria para desarrollo (base de datos MySQL, phpMyAdmin y Mailhog para pruebas de correo) se levanta con Docker Compose.

1. Ve a la carpeta `docker`:

```bash
cd docker
```

2. Ejecuta Docker Compose:

```bash
docker-compose up -d
```

Esto iniciará:
- **MySQL** en el puerto `3307`
- **phpMyAdmin** en el puerto `8080`
- **Mailhog** en los puertos `1025` (SMTP) y `8025` (web)

> **Nota:** Mailhog se utiliza solo para desarrollo local y pruebas de envío de correos.

3. Espera unos segundos a que MySQL esté listo antes de lanzar la aplicación Flask.

4. Vuelve a la raíz del proyecto y ejecuta la aplicación:

```bash
cd ..
python app.py
```

---

## 🧪 Usuarios de ejemplo

Puedes acceder con cualquiera de los siguientes correos, **todas las contraseñas son `123`**:


| Nombre | Apellido(s)        | Email                      | Admin  |
|--------|--------------------|----------------------------|--------|
| Pedro  | Lopez Ruiz         | pedro.lopez@example.com    | USUARIO ESTÁNDAR  |
| Laura  | Pérez              | laura.perez@example.com    | ADMIN   |
| Laura  | García Pérez       | laura.garcia@example.com   | USUARIO ESTÁNDAR  |
| Laura  | Martínez Jiménez   | laura.martinez@example.com | USUARIO ESTÁNDAR  |
| Maria  | García Jiménez     | maria.garcia@example.com   | USUARIO ESTÁNDAR  |
| David  | García             | david.garcia@example.com   | USUARIO ESTÁNDAR  |
| Marta  | Pérez              | marta.perez@example.com    | USUARIO ESTÁNDAR  |
| Laura  | Rodríguez          | laura.rodriguez@example.com| USUARIO ESTÁNDAR  |
| Laura  | González           | laura.gonzalez@example.com | USUARIO ESTÁNDAR  |
| Luis   | González Jiménez   | luis.gonzalez@example.com  | USUARIO ESTÁNDAR  |


---

## 📬 Pruebas de correo

- **Mailhog** está disponible en [http://localhost:8025](http://localhost:8025) para ver todos los correos enviados en local.
- **phpMyAdmin** para gestión de base de datos: [http://localhost:8080](http://localhost:8080)  
  Usuario: `root`  
  Contraseña: `123`

