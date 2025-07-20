from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importar modelos dentro del contexto de la aplicación
with app.app_context():
    from models import Proveedor, ProductoProveedor

    def get_or_create_proveedor(nombre, identificacion, tipo, direccion, telefono, email):
        proveedor = Proveedor.query.filter_by(identificacion=identificacion).first()
        if proveedor:
            print(f"Proveedor {nombre} ya existe con identificación {identificacion}")
            return proveedor, False
        proveedor = Proveedor(
            nombre=nombre,
            identificacion=identificacion,
            tipo=tipo,
            direccion=direccion,
            telefono=telefono,
            email=email,
            activo=True
        )
        db.session.add(proveedor)
        return proveedor, True

    def get_or_create_producto_proveedor(proveedor_id, nombre, descripcion, costo, stock):
        producto = ProductoProveedor.query.filter_by(proveedor_id=proveedor_id, nombre=nombre).first()
        if producto:
            print(f"Producto {nombre} ya existe para el proveedor ID {proveedor_id}")
            return producto, False
        producto = ProductoProveedor(
            proveedor_id=proveedor_id,
            nombre=nombre,
            descripcion=descripcion,
            costo=costo,
            stock=stock,
            activo=True
        )
        db.session.add(producto)
        return producto, True

    def seed_proveedores():
        try:
            # Lista de proveedores con datos realistas
            proveedores_data = [
                {
                    "nombre": "TechDistribuciones S.A.",
                    "identificacion": "1234567890",
                    "tipo": "empresa",
                    "direccion": "Av. Tecnológica 123, Bogotá, Colombia",
                    "telefono": "6015551234",
                    "email": "contacto@techdistribuciones.com",
                    "productos": [
                        {"nombre": "Smartphone Galaxy A54", "descripcion": "Teléfono 5G con 128GB", "costo": 800000, "stock": 50},
                        {"nombre": "Laptop Core i5 11th", "descripcion": "Portátil con 8GB RAM y 512GB SSD", "costo": 2500000, "stock": 20},
                    ]
                },
                {
                    "nombre": "ElectroHogar Ltda.",
                    "identificacion": "0987654321",
                    "tipo": "empresa",
                    "direccion": "Calle 45 #12-34, Medellín, Colombia",
                    "telefono": "6044445678",
                    "email": "ventas@electrohogar.com",
                    "productos": [
                        {"nombre": "Televisor LED 55''", "descripcion": "Smart TV 4K UHD", "costo": 1800000, "stock": 30},
                        {"nombre": "Nevera No Frost 300L", "descripcion": "Refrigerador con dispensador de agua", "costo": 2200000, "stock": 15},
                    ]
                },
                {
                    "nombre": "Juan Pérez",
                    "identificacion": "12345678",
                    "tipo": "persona",
                    "direccion": "Carrera 10 #5-67, Cali, Colombia",
                    "telefono": "6023339876",
                    "email": "juanperez@gmail.com",
                    "productos": [
                        {"nombre": "Audífonos Bluetooth", "descripcion": "Inalámbricos con cancelación de ruido", "costo": 150000, "stock": 100},
                        {"nombre": "Smartwatch Serie 5", "descripcion": "Reloj inteligente con monitor de salud", "costo": 600000, "stock": 40},
                    ]
                },
            ]

            proveedores_creados = 0
            productos_creados = 0

            for proveedor_data in proveedores_data:
                # Crear o recuperar proveedor
                proveedor, creado = get_or_create_proveedor(
                    nombre=proveedor_data["nombre"],
                    identificacion=proveedor_data["identificacion"],
                    tipo=proveedor_data["tipo"],
                    direccion=proveedor_data["direccion"],
                    telefono=proveedor_data["telefono"],
                    email=proveedor_data["email"]
                )
                if creado:
                    proveedores_creados += 1
                db.session.flush()  # Obtener el ID del proveedor

                # Crear productos asociados
                for producto_data in proveedor_data["productos"]:
                    producto, creado = get_or_create_producto_proveedor(
                        proveedor_id=proveedor.id,
                        nombre=producto_data["nombre"],
                        descripcion=producto_data["descripcion"],
                        costo=producto_data["costo"],
                        stock=producto_data["stock"]
                    )
                    if creado:
                        productos_creados += 1

            db.session.commit()
            print(f"Se crearon {proveedores_creados} proveedores y {productos_creados} productos exitosamente.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            print(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        seed_proveedores()