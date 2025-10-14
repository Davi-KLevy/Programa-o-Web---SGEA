from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='home'), # A rota '' (raiz) será a 'home'
]