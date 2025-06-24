from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('almacen', 'Almacén'),
        ('compras', 'Compras'),
    )
    id_usuario = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def categorias_default(cls):
        return [
            {'nombre': 'Verduras', 'descripcion': 'Vegetales frescos'},
            {'nombre': 'Frutas', 'descripcion': 'Frutas frescas'},
            {'nombre': 'Arroz y granos', 'descripcion': 'Granos y cereales'},
            {'nombre': 'Lácteos', 'descripcion': 'Productos lácteos'},
            {'nombre': 'Carnes', 'descripcion': 'Carnes y embutidos'}
        ]
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    nit = models.CharField(max_length=20, unique=True)
    productos_suministrados = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    @classmethod
    def proveedores_default(cls):
        return [
            {'nombre': 'Proveedor 1', 'contacto': 'contacto@proveedor1.com'},
            {'nombre': 'Proveedor 2', 'contacto': 'contacto@proveedor2.com'},
            {'nombre': 'Proveedor 3', 'contacto': 'contacto@proveedor3.com'}
        ]
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class Almacen(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=20, unique=True)
    ubicacion = models.TextField()
    capacidad = models.CharField(max_length=50)
    responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero})"
    
    class Meta:
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'

class Producto(models.Model):
    UNIDAD_CHOICES = [
        ('kg', 'Kilogramo'),
        ('ml', 'Mililitro'),
        ('litro', 'Litro'),
        ('unidad', 'Unidad'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, choices=UNIDAD_CHOICES)
    sku = models.CharField(max_length=100, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'