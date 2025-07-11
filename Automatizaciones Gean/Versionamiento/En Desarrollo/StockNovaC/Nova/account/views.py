from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from utils.gestor_usuarios import validar_usuario
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Producto, Categoria, Proveedor
from .forms import ProductoForm
from django.contrib import messages
from utils.gestor_productos import guardar_producto, obtener_productos, actualizar_producto, eliminar_producto
from django.http import Http404


MONEDAS = [
    {'codigo': 'USD', 'nombre': 'Dólar estadounidense'},
    {'codigo': 'COP', 'nombre': 'Peso colombiano'},
    {'codigo': 'EUR', 'nombre': 'Euro'}
]

CATEGORIAS = [
    {'id': 1, 'nombre': 'Verduras'},
    {'id': 2, 'nombre': 'Frutas'},
    {'id': 3, 'nombre': 'Arroz y granos'},
    {'id': 4, 'nombre': 'Lácteos'},
    {'id': 5, 'nombre': 'Carnes'}
]

PROVEEDORES = [
    {'id': 1, 'nombre': 'Proveedor 1'},
    {'id': 2, 'nombre': 'Proveedor 2'},
    {'id': 3, 'nombre': 'Proveedor 3'}
]

def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if validar_usuario(username, password):
            return redirect('dashboard')  # Redirige al dashboard en lugar de productos_listar
        else:
            error = "Usuario no registrado o credenciales incorrectas."
            
    return render(request, 'account/login.html', {'error': error})

def construction_view(request):
    return user_login(request)  # Reutiliza la misma lógica




# CRUD DE PRODUCTOS
def dashboard(request):
    return render(request, 'account/dashboard.html')




def producto_crear(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        producto_data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'categoria_id': int(request.POST.get('categoria')),
            'precio_unitario': float(request.POST.get('precio_unitario')),
            'cantidad': int(request.POST.get('cantidad')),
            'unidad': request.POST.get('unidad_medida'),
            'sku': request.POST.get('codigo_barras'),  # Usamos código de barras como SKU
            'proveedor_id': int(request.POST.get('proveedor')),
            'estado': request.POST.get('estado') == 'activo'
        }
        
        guardar_producto(producto_data)
        messages.success(request, '¡Producto creado exitosamente!')
        return redirect('productos_listar')

    # Si es GET, mostrar el formulario vacío
    context = {
        'categorias': CATEGORIAS,
        'proveedores': PROVEEDORES,
        'monedas': MONEDAS,
    }
    return render(request, 'account/productos.html', context)

def productos_listar(request):
    """Muestra la lista completa de productos"""
    try:
        productos = obtener_productos()
        
        # Enriquecer con nombres de categorías y proveedores
        categorias_dict = {c['id']: c for c in CATEGORIAS}
        proveedores_dict = {p['id']: p for p in PROVEEDORES}
        
        for producto in productos:
            producto['categoria'] = categorias_dict.get(producto['categoria_id'], {'nombre': 'Desconocida'})
            producto['proveedor'] = proveedores_dict.get(producto['proveedor_id'], {'nombre': 'Desconocido'})
        
        return render(request, 'account/productos_listar.html', {
            'productos': productos,
            'categorias': CATEGORIAS,
            'proveedores': PROVEEDORES
        })
        
    except Exception as e:
        messages.error(request, f"Error al cargar productos: {str(e)}")
        return render(request, 'account/productos_listar.html', {'productos': []})
    
def producto_editar(request, pk):
    try:
        productos = obtener_productos()
        producto = next((p for p in productos if p['id'] == int(pk)), None)
        
        if not producto:
            raise Http404("Producto no encontrado")
        
        if request.method == 'POST':
            # Construir objeto con todos los campos requeridos
            nuevos_datos = {
                'id': int(pk),  # Mantener el mismo ID
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion'),
                'categoria_id': int(request.POST.get('categoria')),
                'precio_unitario': float(request.POST.get('precio_unitario')),
                'cantidad': int(request.POST.get('cantidad')),
                'unidad': request.POST.get('unidad_medida'),
                'sku': request.POST.get('codigo_barras'),
                'proveedor_id': int(request.POST.get('proveedor')),
                'estado': request.POST.get('estado') == 'activo',
                'moneda': request.POST.get('moneda', 'USD')
            }
            
            if actualizar_producto(pk, nuevos_datos):
                messages.success(request, 'Producto actualizado correctamente')
                return redirect('productos_listar')
            else:
                messages.error(request, 'Error al actualizar producto')
        
        context = {
            'producto': producto,
            'categorias': CATEGORIAS,
            'proveedores': PROVEEDORES,
            'monedas': MONEDAS,
            'editar': True
        }
        return render(request, 'account/producto_form.html', context)
    
    except Exception as e:
        messages.error(request, f'Error crítico: {str(e)}')
        return redirect('productos_listar')


def producto_eliminar(request, pk):
    try:
        if request.method == 'POST':
            if eliminar_producto(pk):
                messages.success(request, 'Producto eliminado correctamente')
            else:
                messages.error(request, 'Error al eliminar producto')
            return redirect('productos_listar')
        
        productos = obtener_productos()
        producto = next((p for p in productos if p['id'] == int(pk)), None)
        
        if not producto:
            raise Http404("Producto no encontrado")
        
        return render(request, 'account/producto_confirmar_eliminar.html', {'producto': producto})
    
    except Exception as e:
        messages.error(request, f'Error crítico: {str(e)}')
        return redirect('productos_listar')

def vista_productos(request):
    # Lógica para ver productos o lo que necesites
    productos = Producto.objects.all()
    return render(request, 'account/vista_productos.html', {'productos': productos})