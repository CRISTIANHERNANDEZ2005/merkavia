from extensions import db
from models import Proveedor, ProductoProveedor
from app import app
from sqlalchemy.exc import IntegrityError
import re

# Lista de proveedores predefinidos con sus productos
PROVEEDORES = [
    {
        'nombre': 'Acme Corporation',
        'identificacion': '123456789',
        'tipo': 'empresa',
        'direccion': 'Calle Falsa 123, Ciudad',
        'telefono': '+1234567890',
        'email': 'contacto@acme.com',
        'productos': [
            {
                'nombre': 'Widget A',
                'descripcion': 'Widget de alta calidad para uso industrial',
                'marca': 'Acme',
                'costo': 10.50,
                'stock': 100
            },
            {
                'nombre': 'Widget B',
                'descripcion': 'Widget compacto para uso doméstico',
                'marca': 'Acme',
                'costo': 8.75,
                'stock': 150
            }
        ]
    },
    {
        'nombre': 'Juan Pérez',
        'identificacion': '987654321',
        'tipo': 'persona',
        'direccion': 'Avenida Siempre Viva 742',
        'telefono': '+0987654321',
        'email': 'juan.perez@gmail.com',
        'productos': [
            {
                'nombre': 'Herramienta X',
                'descripcion': 'Herramienta multiusos para carpintería',
                'marca': 'Pérez Tools',
                'costo': 15.00,
                'stock': 50
            }
        ]
    },
    {
        'nombre': 'Tech Supplies S.A.',
        'identificacion': '456789123',
        'tipo': 'empresa',
        'direccion': 'Parque Industrial, Lote 5',
        'telefono': None,
        'email': 'ventas@techsupplies.com',
        'productos': [
            {
                'nombre': 'Cable HDMI 2.0',
                'descripcion': 'Cable HDMI de 3 metros',
                'marca': 'TechSup',
                'costo': 5.25,
                'stock': 200
            },
            {
                'nombre': 'Adaptador USB-C',
                'descripcion': 'Adaptador USB-C a USB-A',
                'marca': 'TechSup',
                'costo': 3.50,
                'stock': 300
            }
        ]
    }
]

def validar_email(email):
    """Valida que el email tenga un formato correcto."""
    if not email:
        return True  # Email es opcional
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validar_identificacion(identificacion):
    """Valida que la identificación sea de 6 a 12 dígitos."""
    return re.match(r'^\d{6,12}$', identificacion) is not None

def validar_telefono(telefono):
    """Valida que el teléfono tenga un formato correcto (opcional)."""
    if not telefono:
        return True  # Teléfono es opcional
    return re.match(r'^\+?\d{7,15}$', telefono) is not None

def validar_datos_proveedor(proveedor):
    """Valida los datos de un proveedor."""
    if not proveedor['nombre']:
        raise ValueError(f"El nombre es obligatorio para el proveedor {proveedor['identificacion']}.")
    if not validar_identificacion(proveedor['identificacion']):
        raise ValueError(f"La identificación {proveedor['identificacion']} debe tener entre 6 y 12 dígitos numéricos.")
    if proveedor['tipo'].lower() not in ['persona', 'empresa']:
        raise ValueError(f"El tipo debe ser 'persona' o 'empresa' para el proveedor {proveedor['nombre']}.")
    if proveedor['telefono'] and not validar_telefono(proveedor['telefono']):
        raise ValueError(f"El teléfono {proveedor['telefono']} no tiene un formato válido.")
    if proveedor['email'] and not validar_email(proveedor['email']):
        raise ValueError(f"El email {proveedor['email']} no tiene un formato válido.")

def validar_datos_producto(producto, proveedor_nombre):
    """Valida los datos de un producto."""
    if not producto['nombre']:
        raise ValueError(f"El nombre es obligatorio para el producto del proveedor {proveedor_nombre}.")
    if not producto['descripcion']:
        raise ValueError(f"La descripción es obligatoria para el producto {producto['nombre']}.")
    if producto['costo'] <= 0:
        raise ValueError(f"El costo debe ser mayor que cero para el producto {producto['nombre']}.")
    if producto['stock'] < 0:
        raise ValueError(f"El stock no puede ser negativo para el producto {producto['nombre']}.")

def cargar_proveedores_y_productos():
    """Carga los proveedores y sus productos predefinidos en la base de datos."""
    with app.app_context():
        for proveedor_data in PROVEEDORES:
            try:
                # Validar datos del proveedor
                validar_datos_proveedor(proveedor_data)

                # Verificar si el proveedor ya existe
                proveedor_existente = Proveedor.query.filter_by(identificacion=proveedor_data['identificacion']).first()
                if proveedor_existente:
                    print(f"Proveedor con identificación {proveedor_data['identificacion']} ya existe. Omitiendo.")
                    continue

                # Crear proveedor
                nuevo_proveedor = Proveedor(
                    nombre=proveedor_data['nombre'],
                    identificacion=proveedor_data['identificacion'],
                    tipo=proveedor_data['tipo'],
                    direccion=proveedor_data['direccion'],
                    telefono=proveedor_data['telefono'],
                    email=proveedor_data['email'],
                    activo=True
                )
                db.session.add(nuevo_proveedor)
                db.session.flush()  # Obtener el ID del proveedor antes de confirmar

                # Agregar productos
                for producto_data in proveedor_data['productos']:
                    # Validar datos del producto
                    validar_datos_producto(producto_data, proveedor_data['nombre'])

                    # Crear producto del proveedor
                    nuevo_producto = ProductoProveedor(
                        proveedor_id=nuevo_proveedor.id,
                        nombre=producto_data['nombre'],
                        descripcion=producto_data['descripcion'],
                        marca=producto_data['marca'],
                        costo=producto_data['costo'],
                        stock=producto_data['stock'],
                        activo=True
                    )
                    db.session.add(nuevo_producto)

                # Confirmar cambios para este proveedor
                db.session.commit()
                print(f"Proveedor '{nuevo_proveedor.nombre}' y sus {len(proveedor_data['productos'])} productos agregados con éxito.")

            except IntegrityError:
                db.session.rollback()
                print(f"Error: La identificación '{proveedor_data['identificacion']}' ya está registrada.")
            except ValueError as ve:
                db.session.rollback()
                print(f"Error en proveedor '{proveedor_data['nombre']}': {str(ve)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error inesperado en proveedor '{proveedor_data['nombre']}': {str(e)}")

def main():
    """Función principal para ejecutar el script."""
    print("Cargando proveedores y productos predefinidos en la base de datos...")
    cargar_proveedores_y_productos()
    print("Proceso finalizado.")

if __name__ == "__main__":
    main()