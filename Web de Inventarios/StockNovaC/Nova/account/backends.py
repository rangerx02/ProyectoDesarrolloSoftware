from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Usa tu validación personalizada
        if validar_usuario(username, password):
            try:
                return Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None