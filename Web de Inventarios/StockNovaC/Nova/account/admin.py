from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Almacen, Proveedor, Categoria, Producto

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'id_usuario', 'rol', 'estado')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('id_usuario', 'rol', 'estado')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Almacen)
admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Producto)