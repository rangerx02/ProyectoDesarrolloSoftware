from django.urls import path
from .views import user_login, vista_productos, dashboard, productos_listar, producto_crear, producto_editar, producto_eliminar
from .views import (lista_usuarios, crear_usuario, lista_almacenes, crear_almacen,
                   lista_proveedores, crear_proveedor, lista_categorias, crear_categoria)

urlpatterns = [
    path('', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('productos/', productos_listar, name='productos_listar'),
    path('productos/vista/', vista_productos, name='vista_productos'),  # Ruta para vista_productos
    path('productos/nuevo/', producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:pk>/', producto_eliminar, name='producto_eliminar'),
    
     # Usuarios
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', crear_usuario, name='crear_usuario'),
    
    # Almacenes
    path('almacenes/', lista_almacenes, name='lista_almacenes'),
    path('almacenes/nuevo/', crear_almacen, name='crear_almacen'),
    
    # Proveedores
    path('proveedores/', lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', crear_proveedor, name='crear_proveedor'),
    
    # Categorías
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categorias/nuevo/', crear_categoria, name='crear_categoria'),
]