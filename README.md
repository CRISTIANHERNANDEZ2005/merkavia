# Tienda Online

Proyecto completo de tienda online desarrollado con Flask, SQLAlchemy y SQLite, con panel de administración, sistema de usuarios, gestión de productos, compras, ventas, reportes y más.

## Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Datos](#modelos-de-datos)
- [Dependencias](#dependencias)
- [Inicialización y Seeders](#inicialización-y-seeders)
- [Migraciones](#migraciones)
- [Vistas y Funcionalidades](#vistas-y-funcionalidades)
- [Recursos Estáticos](#recursos-estáticos)
- [Notas y Recomendaciones](#notas-y-recomendaciones)

---

## Descripción General
Tienda Online es una plataforma web para la gestión y venta de productos, con funcionalidades de carrito de compras, pedidos, administración de inventario, reportes en PDF/Excel, sistema de puntos, y gestión de usuarios y proveedores. Incluye panel de usuario y panel de administración.

## Estructura del Proyecto
```
.
├── app.py                  # Aplicación principal Flask, rutas y lógica de negocio
├── models.py               # Definición de modelos de datos SQLAlchemy
├── requirements.txt        # Dependencias del proyecto
├── extensions.py           # Inicialización de extensiones (db)
├── migration_add_puntos_usados.py # Script de migración manual
├── seed_database.py        # Seeder de proveedores y productos
├── seed_users.py           # Seeder de usuarios, categorías y productos
├── seed_proveedores.py     # Seeder adicional de proveedores
├── instance/database.db    # Base de datos SQLite
├── static/
│   ├── css/styles.css      # Estilos personalizados
│   ├── js/main.js          # Funcionalidad JS
│   └── img/                # Imágenes y logos
└── templates/
    ├── usuario/            # Vistas para usuarios finales
    └── admin/              # Vistas para administración
```

## Modelos de Datos
- **Categoria**: Categorías y subcategorías de productos.
- **Producto**: Productos en venta, con descuentos, stock, marca, proveedor.
- **Proveedor**: Proveedores de productos, con datos de contacto.
- **ProductoProveedor**: Productos ofrecidos por proveedores.
- **Compra / DetalleCompra**: Registro de compras a proveedores.
- **Usuario**: Usuarios registrados, admins y clientes, con sistema de puntos.
- **Carrito**: Carrito de compras por usuario.
- **Pedido / DetallePedido**: Pedidos realizados por usuarios.
- **HistorialPedido**: Cambios de estado de pedidos.
- **Review**: Reseñas de productos por usuarios.

## Dependencias
Principales librerías utilizadas (ver `requirements.txt` para la lista completa):
- Flask, Flask-SQLAlchemy, Flask-CORS
- pdfkit, xhtml2pdf, openpyxl, XlsxWriter, pandas
- Werkzeug, bcrypt, Faker, Jinja2

## Inicialización y Seeders
- **seed_database.py**: Carga proveedores y productos de ejemplo.
- **seed_users.py**: Carga usuarios, categorías, productos y relaciones.
- **seed_proveedores.py**: Carga proveedores y productos adicionales.

Ejecutar los seeders manualmente para poblar la base de datos:
```bash
python seed_database.py
python seed_users.py
python seed_proveedores.py
```

## Migraciones
Las migraciones de la base de datos se manejan manualmente. Ejemplo:
- **migration_add_puntos_usados.py**: Agrega la columna `puntos_usados` a la tabla `Pedido`.

Ejecutar:
```bash
python migration_add_puntos_usados.py
```

## Vistas y Funcionalidades
### Usuario Final (`templates/usuario/`):
- Registro, login, perfil, recuperación de contraseña
- Navegación por categorías y productos
- Carrito de compras, checkout, pedidos, historial
- Reseñas de productos, destacados, ofertas
- Facturación y descarga de facturas

### Administración (`templates/admin/`):
- Dashboard, gestión de usuarios, productos, categorías, proveedores
- Compras, ventas, pedidos, notificaciones
- Reportes en PDF y Excel: inventario, ventas, compras, usuarios, proveedores, categorías
- Descargas de reportes y facturas

#### Reportes disponibles (`templates/admin/reportes/`):
- `categorias_pdf.html`, `productos_pdf.html`, `usuarios_pdf.html`, `compras_pdf.html`, `ventas_pdf.html`, `proveedores_pdf.html`

## Recursos Estáticos
- **CSS**: `static/css/styles.css` (personalización visual)
- **JS**: `static/js/main.js` (funcionalidad interactiva)
- **Imágenes**: `static/img/logo1.jpg`, `static/img/logo2.png`

## Notas y Recomendaciones
- El proyecto utiliza SQLite por defecto, pero puede adaptarse a otros motores SQL.
- Las migraciones deben realizarse manualmente según los scripts proporcionados.
- Para desarrollo, usar entorno virtual y revisar dependencias en `requirements.txt`.
- El diseño es responsive y profesional, con vistas separadas para usuario y administración.

---

**Desarrollado por Cristian** 