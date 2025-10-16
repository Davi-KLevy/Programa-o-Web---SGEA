from django.urls import path
from . import views


urlpatterns = [

    path('', views.login, name='login'), # Rota para a página de login

    path('cadastro/', views.cadastro, name='cadastro'), # Rota para a página de cadastro

    path('principal/', views.principal, name='principal'), # Rota para a página principal

    path('participante/', views.participante, name='participante'), # Rota para a página do participante

    path('organizador/', views.organizador, name='organizador'), # Rota para a página do organizador

]