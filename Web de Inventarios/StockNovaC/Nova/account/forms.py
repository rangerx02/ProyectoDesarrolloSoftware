from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Categoria, Proveedor, Usuario, Almacen

class LoginForm(forms.Form):
    """
    Formulario para el login de usuarios.
    """
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'login__input',
            'autocomplete': 'username',
            'required': 'required'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'login__input',
            'autocomplete': 'current-password',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        for field in self.Meta.fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'Este campo es obligatorio.')
        return cleaned_data
    
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'precio_unitario': 'Precio unitario',
            'cantidad': 'Cantidad',
            'unidad': 'Unidad de medida',
            'sku': 'Código SKU',
            'proveedor': 'Proveedor',
            'estado': 'Estado',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Detergente'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detalles del producto'}),
            'precio_unitario': forms.NumberInput(attrs={'placeholder': 'Ej: 1000.00'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ej: 50'}),
            'unidad': forms.Select(choices=Producto.UNIDAD_CHOICES),
            'sku': forms.TextInput(attrs={'placeholder': 'Ej: PROD-001'}),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
            'categoria': forms.Select(),  # Se llenará desde la vista
            'proveedor': forms.Select(),  # Se llenará desde la vista
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
       
       
#Recien Agregado    
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'id_usuario', 'first_name', 'last_name', 'email', 'rol', 'estado']
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }