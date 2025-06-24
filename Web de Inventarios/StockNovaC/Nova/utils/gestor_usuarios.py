from django.contrib.auth import login
from django.shortcuts import render, redirect
from account.models import Usuario  # Import modificado

def validar_usuario(username, password, archivo='admin.txt'):
    try:
        with open(archivo, 'r') as f:
            for line in f:
                user, passwd = line.strip().split(';')
                if username == user and password == passwd:
                    return True
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado.")
    return False

def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if validar_usuario(username, password):
            user, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'is_active': True,
                    'is_staff': True  # Para acceso al admin
                }
            )
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Credenciales inválidas"
    
    return render(request, 'account/login.html', {'error': error})