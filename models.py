from extensions import db
from datetime import datetime

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    activa = db.Column(db.Boolean, default=True)
    subcategorias = db.relationship('Categoria', 
                                   backref=db.backref('parent', remote_side=[id]),
                                   lazy='dynamic')
    productos = db.relationship('Producto', backref='categoria', lazy=True, cascade='all, delete-orphan')

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=True)
    imagen = db.Column(db.Text, default='https://via.placeholder.com/300')
    stock = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=10)
    stock_maximo = db.Column(db.Integer, default=100)
    stock_reservado = db.Column(db.Integer, default=0)
    destacado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    descuento = db.Column(db.Float, default=0.0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    activo = db.Column(db.Boolean, default=True)

    proveedor = db.relationship('Proveedor', back_populates='productos_tienda')

    @property
    def precio_final(self):
        if self.descuento > 0:
            return self.precio * (1 - self.descuento / 100.0)
        return self.precio

    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    identificacion = db.Column(db.String(20), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    
    productos = db.relationship('ProductoProveedor', back_populates='proveedor', lazy='dynamic')
    productos_tienda = db.relationship('Producto', back_populates='proveedor')
    compras = db.relationship('Compra', back_populates='proveedor', lazy='dynamic')

class ProductoProveedor(db.Model):
    __tablename__ = 'producto_proveedor'
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    marca = db.Column(db.String(50))
    costo = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    es_compra = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    proveedor = db.relationship('Proveedor', back_populates='productos')
    detalles_compra = db.relationship('DetalleCompra', back_populates='producto_proveedor', cascade='all, delete-orphan')

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)  # Nuevo campo para subtotal sin IVA
    total = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    detalles = db.relationship('DetalleCompra', back_populates='compra', lazy=True, cascade='all, delete-orphan')
    proveedor = db.relationship('Proveedor', back_populates='compras')

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto_proveedor.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    convertido = db.Column(db.Boolean, default=False)

    compra = db.relationship('Compra', back_populates='detalles')
    producto_proveedor = db.relationship('ProductoProveedor', back_populates='detalles_compra')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    identificacion = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    puntos = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Usuario {self.email}>'

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    producto = db.relationship('Producto', backref='carritos', lazy='select')

    def __repr__(self):
        return f'<Carrito {self.id}>'

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    puntos_usados = db.Column(db.Integer, default=0)  
    puntos_ganados = db.Column(db.Integer, default=0) 
    usuario = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id}>'

class HistorialPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    estado_anterior = db.Column(db.String(20), nullable=False)
    estado_nuevo = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    pedido = db.relationship('Pedido', backref=db.backref('historial', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('historial_pedidos', lazy=True))

    def __repr__(self):
        return f'<HistorialPedido {self.pedido_id}: {self.estado_anterior} -> {self.estado_nuevo}>'

class DetallePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descuento_aplicado = db.Column(db.Float, default=0.0)
    producto = db.relationship('Producto', backref='detalles_pedido')

    @property
    def precio_final(self):
        return self.precio * (1 - self.descuento_aplicado / 100.0)

    def __repr__(self):
        return f'<DetallePedido {self.id}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    producto = db.relationship('Producto', backref=db.backref('reviews', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('reviews', lazy=True))
    __table_args__ = (
        db.CheckConstraint('calificacion >= 1 AND calificacion <= 5', name='check_calificacion_rango'),
    )
    
    def __repr__(self):
        return f'<Review {self.id}>'