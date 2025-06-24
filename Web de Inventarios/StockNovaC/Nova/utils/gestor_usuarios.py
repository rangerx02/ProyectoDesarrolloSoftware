from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from account.models import Usuario
from django.contrib import messages
import os

def validar_usuario(username, password, archivo='admin.txt'):
    """Valida las credenciales contra el archivo TXT"""
    try:
        # Construye la ruta absoluta al archivo
        file_path = os.path.join(os.path.dirname(__file__), '..', archivo)
        file_path = os.path.abspath(file_path)
        
        with open(file_path, 'r') as f:
            for line in f:
                if ';' in line:  # Verifica que la línea tenga el formato correcto
                    user, passwd = line.strip().split(';')
                    if username == user and password == passwd:
                        return True
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado en {file_path}")
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")
    return False

def user_login(request):
    """Vista personalizada de login que usa el archivo TXT"""
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Primero validamos contra el archivo TXT
        if validar_usuario(username, password):
            # Luego autenticamos con el sistema de Django
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                # Si el usuario no existe en la base de datos, lo creamos
                user = Usuario.objects.create_user(
                    username=username,
                    password=password,  # Importante: guardamos la contraseña correctamente
                    is_active=True,
                    is_staff=True  # Para acceso al admin si es necesario
                )
                user.save()
            
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Credenciales inválidas. Por favor intenta nuevamente."
    
    return render(request, 'account/login.html', {'error': error})