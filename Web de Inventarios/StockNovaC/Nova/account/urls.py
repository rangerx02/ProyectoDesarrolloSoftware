from django.urls import path
""""
from .views import (
    user_login, 
    dashboard,
    # Productos
    productos_listar, producto_crear, producto_editar, producto_eliminar,
    # Usuarios
    lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario,
    # Almacenes
    lista_almacenes, crear_almacen, editar_almacen, eliminar_almacen,
    # Proveedores
    lista_proveedores, crear_proveedor, editar_proveedor, eliminar_proveedor,
    # Categorías
    lista_categorias, crear_categoria, editar_categoria, eliminar_categoria
)
"""
from .views import (
    user_login, user_logout, dashboard,
    lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario,
    lista_proveedores, crear_proveedor, editar_proveedor, eliminar_proveedor,
    lista_categorias, crear_categoria, editar_categoria, eliminar_categoria,
    lista_almacenes, crear_almacen, editar_almacen, eliminar_almacen,
    producto_crear, productos_listar, producto_editar, producto_eliminar
)

urlpatterns = [
    path('', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    #path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    #path('dashboard/', dashboard, name='dashboard'),
    
    # Productos
    path('productos/', productos_listar, name='productos_listar'),
    path('productos/crear/', producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:pk>/', producto_eliminar, name='producto_eliminar'),
    
    # Usuarios
    path('usuarios/', lista_usuarios, name='usuarios_listar'),
    path('usuarios/nuevo/', crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),
    
    # Almacenes
    path('almacenes/', lista_almacenes, name='almacenes_listar'),
    path('almacenes/nuevo/', crear_almacen, name='crear_almacen'),
    path('almacenes/editar/<int:pk>/', editar_almacen, name='editar_almacen'),
    path('almacenes/eliminar/<int:pk>/', eliminar_almacen, name='eliminar_almacen'),
    
    # Proveedores
    path('proveedores/', lista_proveedores, name='proveedores_listar'),
    path('proveedores/nuevo/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', eliminar_proveedor, name='eliminar_proveedor'),
    
    # Categorías
    path('categorias/', lista_categorias, name='categorias_listar'),
    path('categorias/nuevo/', crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', eliminar_categoria, name='eliminar_categoria'),
]