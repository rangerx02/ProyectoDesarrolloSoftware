import os
from django.conf import settings
from datetime import datetime

ARCHIVO_ALMACENES = os.path.join(settings.BASE_DIR, 'almacenes.txt')

def obtener_almacenes():
    almacenes = []
    try:
        if os.path.exists(ARCHIVO_ALMACENES):
            with open(ARCHIVO_ALMACENES, 'r') as f:
                for idx, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    datos = linea.split('|')
                    if len(datos) < 4:
                        continue
                        
                    almacen = {
                        'id': idx,
                        'nombre': datos[0],
                        'ubicacion': datos[1],
                        'responsable': datos[2],
                        'estado': datos[3].lower() == 'true',
                        'fecha_creacion': datos[4] if len(datos) > 4 else datetime.now().isoformat()
                    }
                    almacenes.append(almacen)
    except Exception as e:
        print(f"Error al leer almacenes: {str(e)}")
    
    return almacenes

def guardar_almacen(almacen_data):
    try:
        almacenes = obtener_almacenes()
        nuevo_id = len(almacenes) + 1
        
        with open(ARCHIVO_ALMACENES, 'a+') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(f.tell() - 1)
                if f.read(1) != '\n':
                    f.write('\n')
            
            linea = (
                f"{almacen_data.get('nombre', '')}|"
                f"{almacen_data.get('ubicacion', '')}|"
                f"{almacen_data.get('responsable', '')}|"
                f"{almacen_data.get('estado', True)}|"
                f"{datetime.now().isoformat()}\n"
            )
            f.write(linea)
        return True
    except Exception as e:
        print(f"Error al guardar almacén: {str(e)}")
        return False

def actualizar_almacen(almacen_id, nuevos_datos):
    try:
        almacenes = obtener_almacenes()
        almacen_id = int(almacen_id)
        
        for i, almacen in enumerate(almacenes):
            if almacen['id'] == almacen_id:
                almacenes[i] = {
                    'id': almacen_id,
                    'nombre': nuevos_datos.get('nombre', almacen['nombre']),
                    'ubicacion': nuevos_datos.get('ubicacion', almacen['ubicacion']),
                    'responsable': nuevos_datos.get('responsable', almacen['responsable']),
                    'estado': nuevos_datos.get('estado', almacen['estado']),
                    'fecha_creacion': almacen['fecha_creacion']
                }
                
                with open(ARCHIVO_ALMACENES, 'w') as f:
                    for a in almacenes:
                        linea = (
                            f"{a['nombre']}|{a['ubicacion']}|{a['responsable']}|"
                            f"{a['estado']}|{a['fecha_creacion']}\n"
                        )
                        f.write(linea)
                return True
        return False
    except Exception as e:
        print(f"Error al actualizar almacén: {str(e)}")
        return False

def eliminar_almacen(almacen_id):
    try:
        almacenes = obtener_almacenes()
        almacen_id = int(almacen_id)
        
        almacenes_actualizados = [a for a in almacenes if a['id'] != almacen_id]
        
        if len(almacenes_actualizados) == len(almacenes):
            return False
            
        with open(ARCHIVO_ALMACENES, 'w') as f:
            for new_id, almacen in enumerate(almacenes_actualizados, start=1):
                almacen['id'] = new_id
                linea = (
                    f"{almacen['nombre']}|{almacen['ubicacion']}|{almacen['responsable']}|"
                    f"{almacen['estado']}|{almacen['fecha_creacion']}\n"
                )
                f.write(linea)
        return True
    except Exception as e:
        print(f"Error al eliminar almacén: {str(e)}")
        return False