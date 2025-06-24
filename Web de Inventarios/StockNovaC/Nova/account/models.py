from django.db import models
from django.utils import timezone

# Modelo para Categoría con datos predefinidos
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

# Modelo para Proveedor con datos predefinidos
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @classmethod
    def proveedores_default(cls):
        return [
            {'nombre': 'Proveedor 1', 'contacto': 'contacto@proveedor1.com'},
            {'nombre': 'Proveedor 2', 'contacto': 'contacto@proveedor2.com'},
            {'nombre': 'Proveedor 3', 'contacto': 'contacto@proveedor3.com'}
        ]

# Modelo para Producto
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
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"