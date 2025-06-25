from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Producto, Categoria, Proveedor, Almacen

class LoginForm(forms.Form):
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

class UsuarioForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=50)
    nombre_completo = forms.CharField(label='Nombre completo', max_length=100)
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        required=False
    )
    rol = forms.ChoiceField(
        label='Rol',
        choices=[('admin', 'Administrador'), ('almacen', 'Almacén')]
    )
    estado = forms.BooleanField(
        label='Activo',
        initial=True,
        required=False,
        widget=forms.CheckboxInput
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password and not self.instance:
            raise ValidationError("La contraseña es obligatoria para nuevos usuarios")
        return password

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