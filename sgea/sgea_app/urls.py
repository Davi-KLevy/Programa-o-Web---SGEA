"""
sgea_app/urls.py - URLs da aplicação
"""

from django.urls import path
from . import views

app_name = 'sgea_app'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Usuários
    path('cadastro/', views.usuario_cadastro, name='usuario_cadastro'),
    path('login/', views.usuario_login, name='login'),
    path('logout/', views.usuario_logout, name='logout'),
    path('perfil/', views.usuario_perfil, name='perfil'),
    
    # Eventos
    path('eventos/', views.eventos_lista, name='eventos_lista'),
    path('eventos/cadastro/', views.evento_cadastro, name='evento_cadastro'),
    path('eventos/<int:evento_id>/', views.evento_detalhes, name='evento_detalhes'),
    
    # Inscrições
    path('eventos/<int:evento_id>/inscrever/', views.inscricao_criar, name='inscricao_criar'),
    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
    
    # Auditoria
    path('auditoria/', views.auditoria_logs, name='auditoria_logs'),
]