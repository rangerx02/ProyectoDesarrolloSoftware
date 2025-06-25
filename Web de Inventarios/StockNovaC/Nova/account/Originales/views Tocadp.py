from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .decorators import login_required_custom
from .forms import UsuarioForm, AlmacenForm, ProveedorForm, CategoriaForm, ProductoForm
#from utils.gestor_usuarios import validar_usuario
from utils.gestor_productos import guardar_producto, obtener_productos, actualizar_producto, eliminar_producto
import os
from .gestor_usuariosCreados import GestorUsuariosCreados


# Crear usuario
success, message = GestorUsuariosCreados.crear_usuario(
    username='nuevo_user',
    nombre='Nombre Completo',
    password='segura123',
    rol='almacen'
)

# Validar credenciales
valid, usuario = GestorUsuariosCreados.validar_credenciales(username, password)

# Obtener todos los usuarios
usuarios = GestorUsuariosCreados.obtener_usuarios()
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

USUARIOS_FILE = os.path.join(DATA_DIR, 'usuarios.txt')
PROVEEDORES_FILE = os.path.join(DATA_DIR, 'proveedores.txt')
CATEGORIAS_FILE = os.path.join(DATA_DIR, 'categorias.txt')
ALMACENES_FILE = os.path.join(DATA_DIR, 'almacenes.txt')

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

def leer_datos(archivo):
    datos = []
    try:
        with open(archivo, 'r') as f:
            for line in f:
                if line.strip():
                    partes = line.strip().split(';')
                    item = {
                        'id': int(partes[0]),
                        'nombre': partes[1],
                        'estado': partes[2] == 'True' if len(partes) > 2 else True
                    }
                    if archivo == USUARIOS_FILE and len(partes) > 3:
                        item['rol'] = partes[3]
                    datos.append(item)
    except FileNotFoundError:
        pass
    return datos

def guardar_datos(archivo, datos):
    with open(archivo, 'w') as f:
        for item in datos:
            linea = f"{item['id']};{item['nombre']};{item.get('estado', True)}"
            if archivo == USUARIOS_FILE and 'rol' in item:
                linea += f";{item['rol']}"
            f.write(linea + '\n')

def obtener_siguiente_id(datos):
    return max([item['id'] for item in datos], default=0) + 1

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if validar_usuario(username, password):
            request.session['usuario_autenticado'] = True
            request.session['username'] = username
            messages.success(request, '¡Bienvenido!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'account/login.html')

def user_logout(request):
    request.session.flush()
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required_custom
def dashboard(request):
    return render(request, 'account/dashboard.html', {
        'username': request.session.get('username', 'Invitado')
    })

@login_required_custom
def lista_usuarios(request):
    usuarios = leer_datos(USUARIOS_FILE)
    return render(request, 'account/usuarios_lista.html', {
        'usuarios': usuarios,
        'titulo': 'Lista de Usuarios'
    })

@login_required_custom
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuarios = leer_datos(USUARIOS_FILE)
            nuevo_usuario = {
                'id': obtener_siguiente_id(usuarios),
                'nombre': form.cleaned_data['username'],
                'rol': form.cleaned_data['rol'],
                'estado': form.cleaned_data['estado']
            }
            usuarios.append(nuevo_usuario)
            guardar_datos(USUARIOS_FILE, usuarios)
            messages.success(request, 'Usuario creado exitosamente!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'account/usuario_form.html', {
        'form': form,
        'titulo': 'Nuevo Usuario',
        'monedas': MONEDAS
    })

@login_required_custom
def editar_usuario(request, pk):
    usuarios = leer_datos(USUARIOS_FILE)
    usuario = next((u for u in usuarios if u['id'] == int(pk)), None)
    if not usuario:
        raise Http404("Usuario no encontrado")
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario['nombre'] = form.cleaned_data['username']
            usuario['rol'] = form.cleaned_data['rol']
            usuario['estado'] = form.cleaned_data['estado']
            guardar_datos(USUARIOS_FILE, usuarios)
            messages.success(request, 'Usuario actualizado!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(initial={
            'username': usuario['nombre'],
            'rol': usuario.get('rol', 'almacen'),
            'estado': usuario['estado']
        })
    return render(request, 'account/usuario_form.html', {
        'form': form,
        'titulo': 'Editar Usuario',
        'monedas': MONEDAS
    })

@login_required_custom
def eliminar_usuario(request, pk):
    usuarios = leer_datos(USUARIOS_FILE)
    usuario = next((u for u in usuarios if u['id'] == int(pk)), None)
    if not usuario:
        raise Http404("Usuario no encontrado")
    if request.method == 'POST':
        usuarios = [u for u in usuarios if u['id'] != int(pk)]
        guardar_datos(USUARIOS_FILE, usuarios)
        messages.success(request, 'Usuario eliminado!')
        return redirect('lista_usuarios')
    return render(request, 'account/usuario_confirmar_eliminar.html', {
        'usuario': usuario
    })

@login_required_custom
def lista_proveedores(request):
    proveedores = leer_datos(PROVEEDORES_FILE)
    return render(request, 'account/proveedores_lista.html', {
        'proveedores': proveedores,
        'titulo': 'Lista de Proveedores'
    })

@login_required_custom
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedores = leer_datos(PROVEEDORES_FILE)
            nuevo_proveedor = {
                'id': obtener_siguiente_id(proveedores),
                'nombre': form.cleaned_data['nombre'],
                'estado': True
            }
            proveedores.append(nuevo_proveedor)
            guardar_datos(PROVEEDORES_FILE, proveedores)
            messages.success(request, 'Proveedor creado!')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'account/proveedor_form.html', {
        'form': form,
        'titulo': 'Nuevo Proveedor'
    })

@login_required_custom
def editar_proveedor(request, pk):
    proveedores = leer_datos(PROVEEDORES_FILE)
    proveedor = next((p for p in proveedores if p['id'] == int(pk)), None)
    if not proveedor:
        raise Http404("Proveedor no encontrado")
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor['nombre'] = form.cleaned_data['nombre']
            guardar_datos(PROVEEDORES_FILE, proveedores)
            messages.success(request, 'Proveedor actualizado!')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(initial={
            'nombre': proveedor['nombre']
        })
    return render(request, 'account/proveedor_form.html', {
        'form': form,
        'titulo': 'Editar Proveedor'
    })

@login_required_custom
def eliminar_proveedor(request, pk):
    proveedores = leer_datos(PROVEEDORES_FILE)
    proveedor = next((p for p in proveedores if p['id'] == int(pk)), None)
    if not proveedor:
        raise Http404("Proveedor no encontrado")
    if request.method == 'POST':
        proveedores = [p for p in proveedores if p['id'] != int(pk)]
        guardar_datos(PROVEEDORES_FILE, proveedores)
        messages.success(request, 'Proveedor eliminado!')
        return redirect('lista_proveedores')
    return render(request, 'account/proveedor_confirmar_eliminar.html', {
        'proveedor': proveedor
    })

@login_required_custom
def lista_categorias(request):
    categorias = leer_datos(CATEGORIAS_FILE)
    return render(request, 'account/categorias_lista.html', {
        'categorias': categorias,
        'titulo': 'Lista de Categorías'
    })

@login_required_custom
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categorias = leer_datos(CATEGORIAS_FILE)
            nueva_categoria = {
                'id': obtener_siguiente_id(categorias),
                'nombre': form.cleaned_data['nombre'],
                'estado': True
            }
            categorias.append(nueva_categoria)
            guardar_datos(CATEGORIAS_FILE, categorias)
            messages.success(request, 'Categoría creada!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'account/categoria_form.html', {
        'form': form,
        'titulo': 'Nueva Categoría'
    })

@login_required_custom
def editar_categoria(request, pk):
    categorias = leer_datos(CATEGORIAS_FILE)
    categoria = next((c for c in categorias if c['id'] == int(pk)), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria['nombre'] = form.cleaned_data['nombre']
            guardar_datos(CATEGORIAS_FILE, categorias)
            messages.success(request, 'Categoría actualizada!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(initial={
            'nombre': categoria['nombre']
        })
    return render(request, 'account/categoria_form.html', {
        'form': form,
        'titulo': 'Editar Categoría'
    })

@login_required_custom
def eliminar_categoria(request, pk):
    categorias = leer_datos(CATEGORIAS_FILE)
    categoria = next((c for c in categorias if c['id'] == int(pk)), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    if request.method == 'POST':
        categorias = [c for c in categorias if c['id'] != int(pk)]
        guardar_datos(CATEGORIAS_FILE, categorias)
        messages.success(request, 'Categoría eliminada!')
        return redirect('lista_categorias')
    return render(request, 'account/categoria_confirmar_eliminar.html', {
        'categoria': categoria
    })

@login_required_custom
def lista_almacenes(request):
    almacenes = leer_datos(ALMACENES_FILE)
    return render(request, 'account/almacenes_lista.html', {
        'almacenes': almacenes,
        'titulo': 'Lista de Almacenes'
    })

@login_required_custom
def crear_almacen(request):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            almacenes = leer_datos(ALMACENES_FILE)
            nuevo_almacen = {
                'id': obtener_siguiente_id(almacenes),
                'nombre': form.cleaned_data['nombre'],
                'estado': True
            }
            almacenes.append(nuevo_almacen)
            guardar_datos(ALMACENES_FILE, almacenes)
            messages.success(request, 'Almacén creado!')
            return redirect('lista_almacenes')
    else:
        form = AlmacenForm()
    return render(request, 'account/almacen_form.html', {
        'form': form,
        'titulo': 'Nuevo Almacén'
    })

@login_required_custom
def editar_almacen(request, pk):
    almacenes = leer_datos(ALMACENES_FILE)
    almacen = next((a for a in almacenes if a['id'] == int(pk)), None)
    if not almacen:
        raise Http404("Almacén no encontrado")
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            almacen['nombre'] = form.cleaned_data['nombre']
            guardar_datos(ALMACENES_FILE, almacenes)
            messages.success(request, 'Almacén actualizado!')
            return redirect('lista_almacenes')
    else:
        form = AlmacenForm(initial={
            'nombre': almacen['nombre']
        })
    return render(request, 'account/almacen_form.html', {
        'form': form,
        'titulo': 'Editar Almacén'
    })

@login_required_custom
def eliminar_almacen(request, pk):
    almacenes = leer_datos(ALMACENES_FILE)
    almacen = next((a for a in almacenes if a['id'] == int(pk)), None)
    if not almacen:
        raise Http404("Almacén no encontrado")
    if request.method == 'POST':
        almacenes = [a for a in almacenes if a['id'] != int(pk)]
        guardar_datos(ALMACENES_FILE, almacenes)
        messages.success(request, 'Almacén eliminado!')
        return redirect('lista_almacenes')
    return render(request, 'account/almacen_confirmar_eliminar.html', {
        'almacen': almacen
    })

@login_required_custom
def producto_crear(request):
    if request.method == 'POST':
        producto_data = {
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'categoria_id': int(request.POST.get('categoria')),
            'precio_unitario': float(request.POST.get('precio_unitario')),
            'cantidad': int(request.POST.get('cantidad')),
            'unidad': request.POST.get('unidad_medida'),
            'sku': request.POST.get('codigo_barras'),
            'proveedor_id': int(request.POST.get('proveedor')),
            'estado': request.POST.get('estado') == 'activo'
        }
        guardar_producto(producto_data)
        messages.success(request, '¡Producto creado exitosamente!')
        return redirect('productos_listar')
    context = {
        'categorias': CATEGORIAS,
        'proveedores': PROVEEDORES,
        'monedas': MONEDAS,
    }
    return render(request, 'account/productos.html', context)

@login_required_custom
def productos_listar(request):
    try:
        productos = obtener_productos()
        
        # Crear diccionarios para mapear IDs a nombres
        categorias_map = {c['id']: c['nombre'] for c in CATEGORIAS}
        proveedores_map = {p['id']: p['nombre'] for p in PROVEEDORES}
        
        # Enriquecer los productos con nombres de categoría y proveedor
        for producto in productos:
            producto['categoria_nombre'] = categorias_map.get(producto['categoria_id'], 'Desconocida')
            producto['proveedor_nombre'] = proveedores_map.get(producto['proveedor_id'], 'Desconocido')
            # Corregir estado (por si hay errores de tipeo)
            producto['estado'] = producto.get('estado', True)
            producto['estado_texto'] = 'Activo' if producto['estado'] else 'Inactivo'
        
        return render(request, 'account/productos_listar.html', {
            'productos': productos,
            'categorias': CATEGORIAS,
            'proveedores': PROVEEDORES
        })
        
    except Exception as e:
        messages.error(request, f"Error al cargar productos: {str(e)}")
        return render(request, 'account/productos_listar.html', {'productos': []})

@login_required_custom
def producto_editar(request, pk):
    try:
        productos = obtener_productos()
        producto = next((p for p in productos if p['id'] == int(pk)), None)
        if not producto:
            raise Http404("Producto no encontrado")
        if request.method == 'POST':
            nuevos_datos = {
                'id': int(pk),
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

@login_required_custom
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