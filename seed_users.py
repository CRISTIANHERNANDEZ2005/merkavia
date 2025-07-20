from extensions import db
from models import Proveedor, Producto, Categoria
from app import app
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Primero definimos las categorías y subcategorías
CATEGORIAS = [
    {
        'nombre': 'Electrónica',
        'subcategorias': ['Celulares', 'Portátiles', 'Televisores', 'Accesorios Electrónicos']
    },
    {
        'nombre': 'Hogar',
        'subcategorias': ['Herramientas', 'Electrodomésticos', 'Muebles']
    }
]

# Lista de proveedores
PROVEEDORES = [
    {
        'nombre': 'Acme Corporation',
        'identificacion': '123456789',
        'tipo': 'empresa',
        'direccion': 'Calle Falsa 123',
        'telefono': '555-1234',
        'email': 'contacto@acme.com'
    },
    {
        'nombre': 'Tech Supplies S.A.',
        'identificacion': '456789123',
        'tipo': 'empresa',
        'direccion': 'Avenida Tecnológica 456',
        'telefono': '555-5678',
        'email': 'ventas@techsupplies.com'
    },
    {
        'nombre': 'Juan Pérez',
        'identificacion': '987654321',
        'tipo': 'persona',
        'direccion': 'Carrera 7 #45-12',
        'telefono': '555-9012',
        'email': 'juan.perez@example.com'
    }
]

# Lista de productos predefinidos con su proveedor y categoría
PRODUCTOS = [
    {
        'nombre': 'Smartphone Galaxy S23',
        'descripcion': 'Teléfono inteligente con 128GB de almacenamiento y cámara de 50MP',
        'precio': 799.99,
        'stock': 50,
        'stock_minimo': 10,
        'stock_maximo': 100,
        'marca': 'Samsung',
        'proveedor_identificacion': '456789123',  # Tech Supplies S.A.
        'categoria_nombre': 'Celulares',  # Subcategoría de Electrónica
        'descuento': 5.0,
        'destacado': True
    },
    {
        'nombre': 'Laptop XPS 13',
        'descripcion': 'Portátil con procesador Intel i7, 16GB RAM y SSD de 512GB',
        'precio': 1299.99,
        'stock': 30,
        'stock_minimo': 5,
        'stock_maximo': 50,
        'marca': 'Dell',
        'proveedor_identificacion': '456789123',  # Tech Supplies S.A.
        'categoria_nombre': 'Portátiles',  # Subcategoría de Electrónica
        'descuento': 0.0,
        'destacado': False
    },
    {
        'nombre': 'Taladro Eléctrico',
        'descripcion': 'Taladro de 600W con velocidad variable y portabrocas de 13mm',
        'precio': 89.99,
        'stock': 40,
        'stock_minimo': 10,
        'stock_maximo': 80,
        'marca': 'Pérez Tools',
        'proveedor_identificacion': '987654321',  # Juan Pérez
        'categoria_nombre': 'Herramientas',  # Subcategoría de Hogar
        'descuento': 10.0,
        'destacado': True
    },
    {
        'nombre': 'Televisor LED 55"',
        'descripcion': 'Televisor 4K UHD con Smart TV y HDR',
        'precio': 499.99,
        'stock': 25,
        'stock_minimo': 5,
        'stock_maximo': 50,
        'marca': 'Acme',
        'proveedor_identificacion': '123456789',  # Acme Corporation
        'categoria_nombre': 'Televisores',  # Subcategoría de Electrónica
        'descuento': 0.0,
        'destacado': False
    },
    {
        'nombre': 'Kit de Destornilladores',
        'descripcion': 'Juego de 6 destornilladores de punta fina para trabajos de precisión',
        'precio': 29.99,
        'stock': 60,
        'stock_minimo': 15,
        'stock_maximo': 100,
        'marca': 'Pérez Tools',
        'proveedor_identificacion': '987654321',  # Juan Pérez
        'categoria_nombre': 'Herramientas',  # Subcategoría de Hogar
        'descuento': 0.0,
        'destacado': False
    },
    {
        'nombre': 'Cable HDMI 3M',
        'descripcion': 'Cable HDMI 2.0 de alta velocidad para conexiones 4K',
        'precio': 12.99,
        'stock': 100,
        'stock_minimo': 20,
        'stock_maximo': 200,
        'marca': 'TechSup',
        'proveedor_identificacion': '456789123',  # Tech Supplies S.A.
        'categoria_nombre': 'Accesorios Electrónicos',  # Subcategoría de Electrónica
        'descuento': 15.0,
        'destacado': True
    }
]

def crear_categorias():
    """Crea las categorías y subcategorías en la base de datos."""
    with app.app_context():
        for categoria_data in CATEGORIAS:
            # Verificar si la categoría principal ya existe
            categoria_principal = Categoria.query.filter_by(
                nombre=categoria_data['nombre'], 
                parent_id=None
            ).first()
            
            if not categoria_principal:
                categoria_principal = Categoria(
                    nombre=categoria_data['nombre'],
                    parent_id=None,
                    activa=True
                )
                db.session.add(categoria_principal)
                db.session.commit()
                print(f"Categoría principal '{categoria_principal.nombre}' creada.")
            
            # Crear subcategorías
            for subcat_nombre in categoria_data['subcategorias']:
                subcategoria = Categoria.query.filter_by(
                    nombre=subcat_nombre,
                    parent_id=categoria_principal.id
                ).first()
                
                if not subcategoria:
                    subcategoria = Categoria(
                        nombre=subcat_nombre,
                        parent_id=categoria_principal.id,
                        activa=True
                    )
                    db.session.add(subcategoria)
                    db.session.commit()
                    print(f"Subcategoría '{subcategoria.nombre}' creada bajo '{categoria_principal.nombre}'.")

def crear_proveedores():
    """Crea los proveedores en la base de datos."""
    with app.app_context():
        for proveedor_data in PROVEEDORES:
            proveedor = Proveedor.query.filter_by(
                identificacion=proveedor_data['identificacion']
            ).first()
            
            if not proveedor:
                proveedor = Proveedor(
                    nombre=proveedor_data['nombre'],
                    identificacion=proveedor_data['identificacion'],
                    tipo=proveedor_data['tipo'],
                    direccion=proveedor_data['direccion'],
                    telefono=proveedor_data['telefono'],
                    email=proveedor_data['email'],
                    activo=True
                )
                db.session.add(proveedor)
                db.session.commit()
                print(f"Proveedor '{proveedor.nombre}' creado.")

def validar_datos_producto(producto, index):
    """Valida los datos de un producto."""
    if not producto['nombre']:
        raise ValueError(f"El nombre es obligatorio para el producto #{index + 1}.")
    if not producto['descripcion']:
        raise ValueError(f"La descripción es obligatoria para el producto '{producto['nombre']}'.")
    if producto['precio'] <= 0:
        raise ValueError(f"El precio debe ser mayor que cero para el producto '{producto['nombre']}'.")
    if producto['stock'] < 0:
        raise ValueError(f"El stock no puede ser negativo para el producto '{producto['nombre']}'.")
    if producto['stock_minimo'] < 0:
        raise ValueError(f"El stock mínimo no puede ser negativo para el producto '{producto['nombre']}'.")
    if producto['stock_maximo'] < producto['stock_minimo']:
        raise ValueError(f"El stock máximo debe ser mayor o igual al stock mínimo para el producto '{producto['nombre']}'.")
    if producto['descuento'] < 0 or producto['descuento'] > 100:
        raise ValueError(f"El descuento debe estar entre 0 y 100 para el producto '{producto['nombre']}'.")

def cargar_productos():
    """Carga los productos predefinidos en la base de datos."""
    with app.app_context():
        for index, producto_data in enumerate(PRODUCTOS):
            try:
                # Validar datos del producto
                validar_datos_producto(producto_data, index)

                # Buscar proveedor por identificación
                proveedor = Proveedor.query.filter_by(identificacion=producto_data['proveedor_identificacion']).first()
                if not proveedor:
                    raise ValueError(f"No se encontró proveedor con identificación {producto_data['proveedor_identificacion']} para el producto '{producto_data['nombre']}'.")

                # Buscar categoría por nombre (debe ser una subcategoría)
                categoria = Categoria.query.filter_by(nombre=producto_data['categoria_nombre'])\
                          .filter(Categoria.parent_id != None)\
                          .first()
                if not categoria:
                    raise ValueError(f"No se encontró la subcategoría '{producto_data['categoria_nombre']}' para el producto '{producto_data['nombre']}'.")

                # Verificar si el producto ya existe (por nombre, marca, categoría y proveedor)
                producto_existente = Producto.query.filter_by(
                    nombre=producto_data['nombre'],
                    marca=producto_data['marca'],
                    categoria_id=categoria.id,
                    proveedor_id=proveedor.id
                ).first()
                if producto_existente:
                    print(f"Producto '{producto_data['nombre']}' con marca '{producto_data['marca']}' ya existe para el proveedor '{proveedor.nombre}'. Omitiendo.")
                    continue

                # Crear producto
                nuevo_producto = Producto(
                    nombre=producto_data['nombre'],
                    descripcion=producto_data['descripcion'],
                    precio=producto_data['precio'],
                    stock=producto_data['stock'],
                    stock_minimo=producto_data['stock_minimo'],
                    stock_maximo=producto_data['stock_maximo'],
                    marca=producto_data['marca'],
                    proveedor_id=proveedor.id,
                    categoria_id=categoria.id,
                    descuento=producto_data['descuento'],
                    destacado=producto_data['destacado'],
                    fecha_creacion=datetime.utcnow(),
                    activo=True,
                    imagen='https://via.placeholder.com/300'
                )
                db.session.add(nuevo_producto)
                db.session.commit()
                print(f"Producto '{nuevo_producto.nombre}' agregado con éxito para el proveedor '{proveedor.nombre}' en la categoría '{categoria.nombre}'.")

            except IntegrityError:
                db.session.rollback()
                print(f"Error: No se pudo agregar el producto '{producto_data['nombre']}' debido a un conflicto en la base de datos.")
            except ValueError as ve:
                db.session.rollback()
                print(f"Error en producto #{index + 1}: {str(ve)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error inesperado en producto '{producto_data['nombre']}': {str(e)}")

def main():
    """Función principal para ejecutar el script."""
    print("Creando estructura de categorías...")
    crear_categorias()
    
    print("\nCreando proveedores...")
    crear_proveedores()
    
    print("\nCargando productos predefinidos en la base de datos...")
    cargar_productos()
    
    print("\nProceso finalizado.")

if __name__ == "__main__":
    main()