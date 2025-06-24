def validar_usuario(username, password, archivo='admin.txt'):
    try:
        with open(archivo, 'r') as f:
            for line in f:
                user, passwd = line.strip().split(';')
                if username == user and password == passwd:
                    return True
    except FileNotFoundError:
        print("Archivo admin.txt no encontrado.")
    return False
