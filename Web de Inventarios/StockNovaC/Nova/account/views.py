from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .decorators import login_required_custom
from .forms import UsuarioForm, AlmacenForm, ProveedorForm, CategoriaForm, ProductoForm, LoginForm
from utils.gestor_productos import guardar_producto, obtener_productos, actualizar_producto, eliminar_producto
from .gestor_usuariosCreados import GestorUsuariosCreados
import os
from django.conf import settings

# Configuración de archivos
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

ADMIN_FILE = os.path.join(DATA_DIR, 'admin.txt')
PROVEEDORES_FILE = os.path.join(DATA_DIR, 'proveedores.txt')
CATEGORIAS_FILE = os.path.join(DATA_DIR, 'categorias.txt')
ALMACENES_FILE = os.path.join(DATA_DIR, 'almacenes.txt')

# Constantes globales
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

# Funciones auxiliares
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
                    datos.append(item)
    except FileNotFoundError:
        pass
    return datos

def guardar_datos(archivo, datos):
    with open(archivo, 'w') as f:
        for item in datos:
            linea = f"{item['id']};{item['nombre']};{item.get('estado', True)}"
            f.write(linea + '\n')

def obtener_siguiente_id(datos):
    return max([item['id'] for item in datos], default=0) + 1

def validar_usuario_admin(username, password):
    try:
        with open(ADMIN_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    user, pwd = line.strip().split(';')
                    if username == user and password == pwd:
                        return True
    except FileNotFoundError:
        pass
    return False

# Vistas de autenticación
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Primero verificar en admin.txt
        try:
            with open('account/admin.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        user, pwd = line.strip().split(';')
                        if username == user and password == pwd:
                            request.session['usuario_autenticado'] = True
                            request.session['username'] = username
                            request.session['user_rol'] = 'admin'
                            messages.success(request, '¡Bienvenido Administrador!')
                            return redirect('dashboard')
        except FileNotFoundError:
            pass
        
        # Si no es admin, verificar en usuarios.txt
        usuarios = GestorUsuariosCreados.obtener_usuarios()
        for usuario in usuarios:
            if (usuario['username'] == username and 
                usuario['password'] == password and 
                usuario['estado']):
                request.session['usuario_autenticado'] = True
                request.session['username'] = username
                request.session['user_rol'] = usuario['rol']
                messages.success(request, '¡Bienvenido!')
                return redirect('dashboard')
        
        messages.error(request, 'Credenciales inválidas o usuario inactivo')
    
    return render(request, 'account/login.html')

def user_logout(request):
    request.session.flush()
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required_custom
def dashboard(request):
    return render(request, 'account/dashboard.html', {
        'username': request.session.get('username', 'Invitado'),
        'rol': request.session.get('user_rol', 'usuario')
    })

# Vistas de usuarios
@login_required_custom
def lista_usuarios(request):
    if request.session.get('user_rol') != 'admin':
        messages.error(request, 'No tienes permiso para ver esta página')
        return redirect('dashboard')
    
    usuarios = GestorUsuariosCreados.obtener_usuarios()
    return render(request, 'account/usuarios_listar.html', {
        'usuarios': usuarios,
        'titulo': 'Lista de Usuarios'
    })

@login_required_custom
def crear_usuario(request):
    if request.session.get('user_rol') != 'admin':
        messages.error(request, 'No tienes permiso para realizar esta acción')
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Procesar datos directamente como en productos
        usuario_data = {
            'username': request.POST.get('username'),
            'nombres': request.POST.get('nombres'),
            'apellidos': request.POST.get('apellidos'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password1'),
            'rol': request.POST.get('rol'),
            'estado': request.POST.get('estado') == 'activo'
        }
        
        success, message = GestorUsuariosCreados.crear_usuario(**usuario_data)
        if success:
            messages.success(request, message)
            return redirect('usuarios_listar')
        messages.error(request, message)
    
    # Pasar las variables necesarias al template
    return render(request, 'account/usuarios.html', {
        'titulo': 'Nuevo Usuario',
        'roles': ['admin', 'almacen', 'ventas']  # Opciones para el select
    })

@login_required_custom
def editar_usuario(request, pk):
    if request.session.get('user_rol') != 'admin':
        messages.error(request, 'No tienes permiso para realizar esta acción')
        return redirect('dashboard')
    
    usuario = GestorUsuariosCreados.obtener_usuario_por_id(int(pk))
    if not usuario:
        raise Http404("Usuario no encontrado")
        
    if request.method == 'POST':
        update_data = {
            'nombres': request.POST.get('nombres'),
            'apellidos': request.POST.get('apellidos'),
            'email': request.POST.get('email'),
            'rol': request.POST.get('rol'),
            'estado': request.POST.get('estado') == 'activo'
        }
        if request.POST.get('password1'):
            update_data['password'] = request.POST.get('password1')
            
        success, message = GestorUsuariosCreados.actualizar_usuario(int(pk), **update_data)
        if success:
            messages.success(request, message)
            return redirect('usuarios_listar')
        messages.error(request, message)
    
    return render(request, 'account/usuarios.html', {
        'usuario': usuario,
        'titulo': 'Editar Usuario',
        'roles': ['admin', 'almacen', 'ventas'],
        'editar': True
    })

@login_required_custom
def eliminar_usuario(request, pk):
    if request.session.get('user_rol') != 'admin':
        messages.error(request, 'No tienes permiso para realizar esta acción')
        return redirect('dashboard')
    
    usuario = GestorUsuariosCreados.obtener_usuario_por_id(int(pk))
    if not usuario:
        raise Http404("Usuario no encontrado")
        
    if request.method == 'POST':
        success, message = GestorUsuariosCreados.eliminar_usuario(int(pk))
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('lista_usuarios')
    
    return render(request, 'account/usuario_confirmar_eliminar.html', {
        'usuario': usuario
    })

# Vistas de productos
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
        
        categorias_map = {c['id']: c['nombre'] for c in CATEGORIAS}
        proveedores_map = {p['id']: p['nombre'] for p in PROVEEDORES}
        
        for producto in productos:
            producto['categoria_nombre'] = categorias_map.get(producto['categoria_id'], 'Desconocida')
            producto['proveedor_nombre'] = proveedores_map.get(producto['proveedor_id'], 'Desconocido')
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

# Vistas para proveedores
@login_required_custom
def lista_proveedores(request):
    proveedores = leer_datos(PROVEEDORES_FILE)
    return render(request, 'account/proveedores_listar.html', {
        'proveedores': proveedores,
        'titulo': 'Lista de Proveedores'
    })

@login_required_custom
def crear_proveedor(request):
    if request.method == 'POST':
        proveedores = leer_datos(PROVEEDORES_FILE)
        nuevo_proveedor = {
            'id': obtener_siguiente_id(proveedores),
            'nombre': request.POST.get('nombre'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
            'direccion': request.POST.get('direccion'),
            'estado': request.POST.get('estado') == 'activo'
        }
        proveedores.append(nuevo_proveedor)
        guardar_datos(PROVEEDORES_FILE, proveedores)
        messages.success(request, 'Proveedor creado exitosamente!')
        return redirect('proveedores_listar')
    
    return render(request, 'account/proveedores.html', {
        'titulo': 'Nuevo Proveedor'
    })

@login_required_custom
def editar_proveedor(request, pk):
    proveedores = leer_datos(PROVEEDORES_FILE)
    proveedor = next((p for p in proveedores if p['id'] == int(pk)), None)
    if not proveedor:
        raise Http404("Proveedor no encontrado")
        
    if request.method == 'POST':
        proveedor.update({
            'nombre': request.POST.get('nombre'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
            'direccion': request.POST.get('direccion'),
            'estado': request.POST.get('estado') == 'activo'
        })
        guardar_datos(PROVEEDORES_FILE, proveedores)
        messages.success(request, 'Proveedor actualizado!')
        return redirect('proveedores_listar')
    
    return render(request, 'account/proveedores.html', {
        'proveedor': proveedor,
        'titulo': 'Editar Proveedor',
        'editar': True
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

# Vistas para categorías
@login_required_custom
def lista_categorias(request):
    categorias = leer_datos(CATEGORIAS_FILE)
    return render(request, 'account/categorias_listar.html', {
        'categorias': categorias,
        'titulo': 'Lista de Categorías'
    })

@login_required_custom
def crear_categoria(request):
    if request.method == 'POST':
        categorias = leer_datos(CATEGORIAS_FILE)
        nueva_categoria = {
            'id': obtener_siguiente_id(categorias),
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion', ''),
            'estado': request.POST.get('estado') == 'activo'
        }
        categorias.append(nueva_categoria)
        guardar_datos(CATEGORIAS_FILE, categorias)
        messages.success(request, 'Categoría creada exitosamente!')
        return redirect('categorias_listar')
    
    return render(request, 'account/categorias.html', {
        'titulo': 'Nueva Categoría'
    })

@login_required_custom
def editar_categoria(request, pk):
    categorias = leer_datos(CATEGORIAS_FILE)
    categoria = next((c for c in categorias if c['id'] == int(pk)), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
        
    if request.method == 'POST':
        categoria.update({
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion', ''),
            'estado': request.POST.get('estado') == 'activo'
        })
        guardar_datos(CATEGORIAS_FILE, categorias)
        messages.success(request, 'Categoría actualizada!')
        return redirect('categorias_listar')
    
    return render(request, 'account/categorias.html', {
        'categoria': categoria,
        'titulo': 'Editar Categoría',
        'editar': True
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

# Vistas para almacenes
@login_required_custom
def lista_almacenes(request):
    almacenes = leer_datos(ALMACENES_FILE)
    return render(request, 'account/almacenes_listar.html', {
        'almacenes': almacenes,
        'titulo': 'Lista de Almacenes'
    })

@login_required_custom
def crear_almacen(request):
    if request.method == 'POST':
        almacenes = leer_datos(ALMACENES_FILE)
        nuevo_almacen = {
            'id': obtener_siguiente_id(almacenes),
            'nombre': request.POST.get('nombre'),
            'direccion': request.POST.get('direccion'),
            'telefono': request.POST.get('telefono'),
            'responsable': request.POST.get('responsable'),
            'estado': request.POST.get('estado') == 'activo'
        }
        almacenes.append(nuevo_almacen)
        guardar_datos(ALMACENES_FILE, almacenes)
        messages.success(request, 'Almacén creado exitosamente!')
        return redirect('almacenes_listar')
    
    # Obtener usuarios para el select de responsable
    usuarios = GestorUsuariosCreados.obtener_usuarios()
    return render(request, 'account/almacenes.html', {
        'titulo': 'Nuevo Almacén',
        'usuarios': usuarios
    })

@login_required_custom
def editar_almacen(request, pk):
    almacenes = leer_datos(ALMACENES_FILE)
    almacen = next((a for a in almacenes if a['id'] == int(pk)), None)
    if not almacen:
        raise Http404("Almacén no encontrado")
        
    if request.method == 'POST':
        almacen.update({
            'nombre': request.POST.get('nombre'),
            'direccion': request.POST.get('direccion'),
            'telefono': request.POST.get('telefono'),
            'responsable': request.POST.get('responsable'),
            'estado': request.POST.get('estado') == 'activo'
        })
        guardar_datos(ALMACENES_FILE, almacenes)
        messages.success(request, 'Almacén actualizado!')
        return redirect('almacenes_listar')
    
    usuarios = GestorUsuariosCreados.obtener_usuarios()
    return render(request, 'account/almacenes.html', {
        'almacen': almacen,
        'titulo': 'Editar Almacén',
        'usuarios': usuarios,
        'editar': True
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