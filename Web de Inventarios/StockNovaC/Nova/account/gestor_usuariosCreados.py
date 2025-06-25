import os
from django.conf import settings

# Configuración de archivos
USUARIOS_FILE = os.path.join(settings.BASE_DIR, 'data', 'usuarios.txt')
os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)

class GestorUsuariosCreados:
    @staticmethod
    def _leer_usuarios():
        usuarios = []
        try:
            with open(USUARIOS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        datos = line.split('|')
                        if len(datos) >= 5:
                            usuarios.append({
                                'id': int(datos[0]),
                                'username': datos[1],
                                'nombre': datos[2],
                                'password': datos[3],
                                'rol': datos[4],
                                'estado': datos[5] == 'True' if len(datos) > 5 else True
                            })
        except FileNotFoundError:
            open(USUARIOS_FILE, 'w').close()
        return usuarios

    @staticmethod
    def _guardar_usuarios(usuarios):
        with open(USUARIOS_FILE, 'w') as f:
            for usuario in usuarios:
                linea = f"{usuario['id']}|{usuario['username']}|{usuario['nombre']}|{usuario['password']}|{usuario['rol']}|{usuario['estado']}"
                f.write(linea + '\n')

    @staticmethod
    def obtener_usuarios():
        return GestorUsuariosCreados._leer_usuarios()

    @staticmethod
    def obtener_usuario_por_id(user_id):
        usuarios = GestorUsuariosCreados._leer_usuarios()
        for usuario in usuarios:
            if usuario['id'] == user_id:
                return usuario
        return None

    @staticmethod
    def obtener_usuario_por_username(username):
        usuarios = GestorUsuariosCreados._leer_usuarios()
        for usuario in usuarios:
            if usuario['username'] == username:
                return usuario
        return None

    @staticmethod
    def crear_usuario(username, nombre, password, rol, estado=True):
        usuarios = GestorUsuariosCreados._leer_usuarios()
        
        if any(u['username'] == username for u in usuarios):
            return False, "El nombre de usuario ya existe"
        
        nuevo_id = max([u['id'] for u in usuarios], default=0) + 1
        
        nuevo_usuario = {
            'id': nuevo_id,
            'username': username,
            'nombre': nombre,
            'password': password,
            'rol': rol,
            'estado': estado
        }
        
        usuarios.append(nuevo_usuario)
        GestorUsuariosCreados._guardar_usuarios(usuarios)
        return True, "Usuario creado exitosamente"

    @staticmethod
    def actualizar_usuario(user_id, **kwargs):
        usuarios = GestorUsuariosCreados._leer_usuarios()
        usuario = next((u for u in usuarios if u['id'] == user_id), None)
        
        if not usuario:
            return False, "Usuario no encontrado"
        
        campos_permitidos = ['nombre', 'rol', 'estado', 'password']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                usuario[campo] = valor
        
        GestorUsuariosCreados._guardar_usuarios(usuarios)
        return True, "Usuario actualizado exitosamente"

    @staticmethod
    def eliminar_usuario(user_id):
        return GestorUsuariosCreados.actualizar_usuario(user_id, estado=False)

    @staticmethod
    def validar_credenciales(username, password):
        usuario = GestorUsuariosCreados.obtener_usuario_por_username(username)
        if usuario and usuario['estado'] and usuario['password'] == password:
            return True, usuario
        return False, None