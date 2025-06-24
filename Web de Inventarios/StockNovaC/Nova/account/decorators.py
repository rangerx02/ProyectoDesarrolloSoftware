from django.shortcuts import redirect

def login_required_custom(view_func):
    """Decorador personalizado para verificar autenticación"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_autenticado'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper