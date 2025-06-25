import os
from django.conf import settings
from datetime import datetime

ARCHIVO_PROVEEDORES = os.path.join(settings.BASE_DIR, 'proveedores.txt')

def obtener_proveedores():
    proveedores = []
    try:
        if os.path.exists(ARCHIVO_PROVEEDORES):
            with open(ARCHIVO_PROVEEDORES, 'r') as f:
                for idx, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    datos = linea.split('|')
                    if len(datos) < 3:
                        continue
                        
                    proveedor = {
                        'id': idx,
                        'nombre': datos[0],
                        'contacto': datos[1],
                        'estado': datos[2].lower() == 'true',
                        'fecha_creacion': datos[3] if len(datos) > 3 else datetime.now().isoformat()
                    }
                    proveedores.append(proveedor)
    except Exception as e:
        print(f"Error al leer proveedores: {str(e)}")
    
    return proveedores

def guardar_proveedor(proveedor_data):
    try:
        proveedores = obtener_proveedores()
        nuevo_id = len(proveedores) + 1
        
        with open(ARCHIVO_PROVEEDORES, 'a+') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(f.tell() - 1)
                if f.read(1) != '\n':
                    f.write('\n')
            
            linea = (
                f"{proveedor_data.get('nombre', '')}|"
                f"{proveedor_data.get('contacto', '')}|"
                f"{proveedor_data.get('estado', True)}|"
                f"{datetime.now().isoformat()}\n"
            )
            f.write(linea)
        return True
    except Exception as e:
        print(f"Error al guardar proveedor: {str(e)}")
        return False

def actualizar_proveedor(proveedor_id, nuevos_datos):
    try:
        proveedores = obtener_proveedores()
        proveedor_id = int(proveedor_id)
        
        for i, proveedor in enumerate(proveedores):
            if proveedor['id'] == proveedor_id:
                proveedores[i] = {
                    'id': proveedor_id,
                    'nombre': nuevos_datos.get('nombre', proveedor['nombre']),
                    'contacto': nuevos_datos.get('contacto', proveedor['contacto']),
                    'estado': nuevos_datos.get('estado', proveedor['estado']),
                    'fecha_creacion': proveedor['fecha_creacion']
                }
                
                with open(ARCHIVO_PROVEEDORES, 'w') as f:
                    for p in proveedores:
                        linea = (
                            f"{p['nombre']}|{p['contacto']}|"
                            f"{p['estado']}|{p['fecha_creacion']}\n"
                        )
                        f.write(linea)
                return True
        return False
    except Exception as e:
        print(f"Error al actualizar proveedor: {str(e)}")
        return False

def eliminar_proveedor(proveedor_id):
    try:
        proveedores = obtener_proveedores()
        proveedor_id = int(proveedor_id)
        
        proveedores_actualizados = [p for p in proveedores if p['id'] != proveedor_id]
        
        if len(proveedores_actualizados) == len(proveedores):
            return False
            
        with open(ARCHIVO_PROVEEDORES, 'w') as f:
            for new_id, proveedor in enumerate(proveedores_actualizados, start=1):
                proveedor['id'] = new_id
                linea = (
                    f"{proveedor['nombre']}|{proveedor['contacto']}|"
                    f"{proveedor['estado']}|{proveedor['fecha_creacion']}\n"
                )
                f.write(linea)
        return True
    except Exception as e:
        print(f"Error al eliminar proveedor: {str(e)}")
        return False