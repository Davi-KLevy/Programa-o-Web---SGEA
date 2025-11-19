from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sgea_app.urls')), # Inclui as URLs da aplicação principal
    path('contas/', include('django.contrib.auth.urls')), # URLs de autenticação (login, logout)
    path('api/', include('api.urls'))
]