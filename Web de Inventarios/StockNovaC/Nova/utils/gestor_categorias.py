import os
from django.conf import settings
from datetime import datetime

ARCHIVO_CATEGORIAS = os.path.join(settings.BASE_DIR, 'categorias.txt')

def obtener_categorias():
    categorias = []
    try:
        if os.path.exists(ARCHIVO_CATEGORIAS):
            with open(ARCHIVO_CATEGORIAS, 'r') as f:
                for idx, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    datos = linea.split('|')
                    if len(datos) < 2:
                        continue
                        
                    categoria = {
                        'id': idx,
                        'nombre': datos[0],
                        'descripcion': datos[1],
                        'estado': datos[2].lower() == 'true' if len(datos) > 2 else True,
                        'fecha_creacion': datos[3] if len(datos) > 3 else datetime.now().isoformat()
                    }
                    categorias.append(categoria)
    except Exception as e:
        print(f"Error al leer categorías: {str(e)}")
    
    return categorias

def guardar_categoria(categoria_data):
    try:
        categorias = obtener_categorias()
        nuevo_id = len(categorias) + 1
        
        with open(ARCHIVO_CATEGORIAS, 'a+') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(f.tell() - 1)
                if f.read(1) != '\n':
                    f.write('\n')
            
            linea = (
                f"{categoria_data.get('nombre', '')}|"
                f"{categoria_data.get('descripcion', '')}|"
                f"{categoria_data.get('estado', True)}|"
                f"{datetime.now().isoformat()}\n"
            )
            f.write(linea)
        return True
    except Exception as e:
        print(f"Error al guardar categoría: {str(e)}")
        return False

def actualizar_categoria(categoria_id, nuevos_datos):
    try:
        categorias = obtener_categorias()
        categoria_id = int(categoria_id)
        
        for i, categoria in enumerate(categorias):
            if categoria['id'] == categoria_id:
                categorias[i] = {
                    'id': categoria_id,
                    'nombre': nuevos_datos.get('nombre', categoria['nombre']),
                    'descripcion': nuevos_datos.get('descripcion', categoria['descripcion']),
                    'estado': nuevos_datos.get('estado', categoria['estado']),
                    'fecha_creacion': categoria['fecha_creacion']
                }
                
                with open(ARCHIVO_CATEGORIAS, 'w') as f:
                    for c in categorias:
                        linea = (
                            f"{c['nombre']}|{c['descripcion']}|"
                            f"{c['estado']}|{c['fecha_creacion']}\n"
                        )
                        f.write(linea)
                return True
        return False
    except Exception as e:
        print(f"Error al actualizar categoría: {str(e)}")
        return False

def eliminar_categoria(categoria_id):
    try:
        categorias = obtener_categorias()
        categoria_id = int(categoria_id)
        
        categorias_actualizadas = [c for c in categorias if c['id'] != categoria_id]
        
        if len(categorias_actualizadas) == len(categorias):
            return False
            
        with open(ARCHIVO_CATEGORIAS, 'w') as f:
            for new_id, categoria in enumerate(categorias_actualizadas, start=1):
                categoria['id'] = new_id
                linea = (
                    f"{categoria['nombre']}|{categoria['descripcion']}|"
                    f"{categoria['estado']}|{categoria['fecha_creacion']}\n"
                )
                f.write(linea)
        return True
    except Exception as e:
        print(f"Error al eliminar categoría: {str(e)}")
        return False