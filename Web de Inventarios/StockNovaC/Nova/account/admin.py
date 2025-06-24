from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Almacen, Proveedor, Categoria, Producto

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'id_usuario', 'rol', 'estado', 'is_staff')
    list_filter = ('rol', 'estado', 'is_staff')
    search_fields = ('username', 'email', 'id_usuario')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('id_usuario', 'rol', 'estado')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('id_usuario', 'rol', 'estado')
        }),
    )

class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero', 'ubicacion', 'responsable', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', 'numero', 'responsable__username')
    raw_id_fields = ('responsable',)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'contacto', 'telefono', 'email', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', 'nit', 'contacto')
    list_per_page = 20

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'categoria', 'precio_unitario', 'cantidad', 'unidad', 'estado')
    list_filter = ('categoria', 'unidad', 'estado')
    search_fields = ('nombre', 'sku', 'descripcion')
    raw_id_fields = ('categoria', 'proveedor', 'almacen')
    list_editable = ('precio_unitario', 'cantidad')
    list_per_page = 30

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)