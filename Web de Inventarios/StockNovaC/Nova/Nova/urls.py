from django.contrib import admin
from django.urls import path, include
## from account.views import user_login, construction_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),  # Conecta las rutas de la app "account"
]