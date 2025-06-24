import os
from django.conf import settings
from datetime import datetime

ARCHIVO_PRODUCTOS = os.path.join(settings.BASE_DIR, 'productos.txt')

def obtener_productos():
    """Lee productos asegurando formato correcto"""
    productos = []
    try:
        if os.path.exists(ARCHIVO_PRODUCTOS):
            with open(ARCHIVO_PRODUCTOS, 'r') as f:
                for idx, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    datos = linea.split('|')
                    if len(datos) < 9:  # Mínimo campos requeridos
                        print(f"Línea {idx} incompleta: {linea}")
                        continue
                        
                    producto = {
                        'id': idx,
                        'nombre': datos[0],
                        'descripcion': datos[1],
                        'categoria_id': int(datos[2]) if datos[2].isdigit() else 0,
                        'precio_unitario': float(datos[3]) if datos[3].replace('.','',1).isdigit() else 0,
                        'cantidad': int(datos[4]) if datos[4].isdigit() else 0,
                        'unidad': datos[5],
                        'sku': datos[6],
                        'proveedor_id': int(datos[7]) if datos[7].isdigit() else 0,
                        'estado': datos[8].lower() == 'true',
                        'fecha_creacion': datos[9] if len(datos) > 9 else datetime.now().isoformat(),
                        'fecha_modificacion': datos[10] if len(datos) > 10 else datetime.now().isoformat()
                    }
                    productos.append(producto)
    except Exception as e:
        print(f"Error crítico al leer: {str(e)}")
    
    return productos

def actualizar_producto(producto_id, nuevos_datos):
    """Actualiza un producto específico en el archivo"""
    try:
        productos = obtener_productos()
        producto_id = int(producto_id)
        
        # Buscar el producto por ID
        for i, producto in enumerate(productos):
            if producto['id'] == producto_id:
                # Mantener campos inmutables
                nuevos_datos['fecha_creacion'] = producto['fecha_creacion']
                nuevos_datos['fecha_modificacion'] = datetime.now().isoformat()
                nuevos_datos['id'] = producto_id
                
                # Actualizar el producto
                productos[i] = nuevos_datos
                
                # Reescribir archivo completo
                with open(ARCHIVO_PRODUCTOS, 'w') as f:
                    for p in productos:
                        linea = (
                            f"{p['nombre']}|{p['descripcion']}|{p['categoria_id']}|"
                            f"{p['precio_unitario']}|{p['cantidad']}|{p['unidad']}|"
                            f"{p['sku']}|{p['proveedor_id']}|{p['estado']}|"
                            f"{p['fecha_creacion']}|{p['fecha_modificacion']}\n"
                        )
                        f.write(linea)
                return True
        return False
    except Exception as e:
        print(f"Error al actualizar producto: {str(e)}")
        return False

def eliminar_producto(producto_id):
    """Elimina un producto del archivo y renumera los IDs"""
    try:
        productos = obtener_productos()
        producto_id = int(producto_id)
        
        # Filtrar el producto a eliminar
        productos_actualizados = [p for p in productos if p['id'] != producto_id]
        
        if len(productos_actualizados) == len(productos):
            return False  # No se eliminó nada
            
        # Reescribir archivo con nuevos IDs secuenciales
        with open(ARCHIVO_PRODUCTOS, 'w') as f:
            for new_id, producto in enumerate(productos_actualizados, start=1):
                producto['id'] = new_id  # Renumerar IDs
                linea = (
                    f"{producto['nombre']}|{producto['descripcion']}|{producto['categoria_id']}|"
                    f"{producto['precio_unitario']}|{producto['cantidad']}|{producto['unidad']}|"
                    f"{producto['sku']}|{producto['proveedor_id']}|{producto['estado']}|"
                    f"{producto['fecha_creacion']}|{datetime.now().isoformat()}\n"
                )
                f.write(linea)
        return True
    except Exception as e:
        print(f"Error al eliminar producto: {str(e)}")
        return False

def guardar_producto(producto_data):
    """Guarda un nuevo producto asegurando formato correcto"""
    try:
        with open(ARCHIVO_PRODUCTOS, 'a+') as f:  # a+ para leer y escribir
            # Verificar si el archivo termina con nueva línea
            f.seek(0, 2)  # Ir al final del archivo
            if f.tell() > 0:  # Si el archivo no está vacío
                f.seek(f.tell() - 1)  # Retroceder un carácter
                if f.read(1) != '\n':
                    f.write('\n')  # Asegurar nueva línea
            
            linea = (
                f"{producto_data.get('nombre', '')}|"
                f"{producto_data.get('descripcion', '')}|"
                f"{producto_data.get('categoria_id', 0)}|"
                f"{producto_data.get('precio_unitario', 0)}|"
                f"{producto_data.get('cantidad', 0)}|"
                f"{producto_data.get('unidad', 'unidad')}|"
                f"{producto_data.get('sku', '')}|"
                f"{producto_data.get('proveedor_id', 0)}|"
                f"{producto_data.get('estado', True)}|"
                f"{datetime.now().isoformat()}|"
                f"{datetime.now().isoformat()}\n"
            )
            f.write(linea)
            f.flush()  # Forzar escritura inmediata
            os.fsync(f.fileno())  # Sincronizar con disco
        return True
    except Exception as e:
        print(f"Error crítico al guardar: {str(e)}")
        return False