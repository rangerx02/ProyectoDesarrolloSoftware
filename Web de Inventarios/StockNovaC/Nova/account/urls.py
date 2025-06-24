from django.urls import path
from .views import user_login, vista_productos, dashboard, productos_listar, producto_crear, producto_editar, producto_eliminar

urlpatterns = [
    path('', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('productos/', productos_listar, name='productos_listar'),
    path('productos/vista/', vista_productos, name='vista_productos'),  # Ruta para vista_productos
    path('productos/nuevo/', producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:pk>/', producto_eliminar, name='producto_eliminar'),
]