from django.urls import path
from . import views

urlpatterns = [
    # Rotas Públicas (Sem necessidade de login)
    path('', views.lista_eventos, name='home'),             # Lista de eventos (Página inicial)
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    
    # Rotas de Usuário Autenticado (Aluno/Professor/Organizador)
    path('dashboard/', views.dashboard, name='dashboard'), # Página inicial após login
    path('inscrever/<int:evento_id>/', views.inscrever_evento, name='inscrever_evento'),
    path('cancelar_inscricao/<int:inscricao_id>/', views.cancelar_inscricao, name='cancelar_inscricao'),
    path('meus_certificados/', views.meus_certificados, name='meus_certificados'),
    
    # Rotas de Organizador (Requer perfil 'Organizador')
    path('eventos/novo/', views.criar_evento, name='criar_evento'),
    path('eventos/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eventos/gerenciar/', views.listar_eventos_organizador, name='gerenciar_eventos'),
    path('evento/<int:evento_id>/inscritos/', views.lista_inscritos, name='lista_inscritos'),
    path('evento/<int:evento_id>/emitir_certificados/', views.emitir_certificados, name='emitir_certificados'),
    path('auditoria/', views.registros_auditoria, name='registros_auditoria'),
]