from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .forms import CadastroUsuarioForm 
# Importe o forms.py que criamos no passo anterior.

# --- Funções Auxiliares de Permissão ---

def is_organizador(user):
    """ Verifica se o usuário é um organizador e está ativo/autenticado. """
    return user.is_authenticated and user.perfil == 'Organizador'

def is_professor_or_organizador(user):
    """ Verifica se o usuário é um professor ou organizador. """
    return user.is_authenticated and user.perfil in ['Professor', 'Organizador']

# --- Rotas Públicas ---

def lista_eventos(request):
    """
    Exibe a lista de todos os eventos (rota: /). 
    Foco em eventos com data_inicial no futuro.
    """
    # Lógica futura: buscar eventos ativos no banco de dados
    return render(request, 'lista_eventos.html', {'eventos': []})

def detalhe_evento(request, evento_id):
    """ 
    Exibe os detalhes de um evento específico (rota: /evento/<id>/). 
    Inclui botão de inscrição se o usuário for Aluno/Professor.
    """
    # Lógica futura: buscar evento pelo ID
    return HttpResponse(f"Detalhes do Evento ID: {evento_id}")

def cadastro_usuario(request):
    """ 
    Formulário para cadastro de novos usuários (rota: /cadastro/). 
    Aplica validações do forms.py, define is_active=False e simula envio de e-mail.
    """
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            # A função save no forms.py já hasheia a senha
            novo_usuario = form.save(commit=False)
            
            # Regra de Negócio: Novo usuário começa como inativo (is_active=False)
            # até a confirmação por e-mail (automação futura).
            novo_usuario.is_active = True 
            novo_usuario.save()
            
            # Lógica futura: Envio de e-mail de confirmação
            
            return render(request, 'cadastro_sucesso.html', {'nome': novo_usuario.nome})
    else:
        form = CadastroUsuarioForm()
        
    # O template 'cadastro_usuario.html' ainda precisa ser criado
    return render(request, 'cadastro_usuario.html', {'form': form})

# --- Rotas de Usuário Autenticado ---

@login_required
def dashboard(request):
    """ 
    Dashboard após o login (rota: /dashboard/). 
    Exibe informações diferentes com base no perfil (Aluno, Professor, Organizador).
    """
    return render(request, 'dashboard.html')

@login_required
def inscrever_evento(request, evento_id):
    """ 
    Realiza a inscrição em um evento (rota: /inscrever/<id>/).
    Apenas Alunos e Professores podem se inscrever.
    """
    # Lógica futura: Verificar se há vagas e se já está inscrito.
    return HttpResponse(f"Processando inscrição no Evento ID: {evento_id}")

@login_required
def cancelar_inscricao(request, inscricao_id):
    """ 
    Cancela uma inscrição (rota: /cancelar_inscricao/<id>/).
    """
    # Lógica futura: Deletar ou inativar a Inscrição.
    return HttpResponse(f"Cancelando Inscrição ID: {inscricao_id}")

@login_required
def meus_certificados(request):
    """ 
    Lista os certificados do usuário (rota: /meus_certificados/).
    Permitido para Alunos e Professores.
    """
    # Lógica futura: Buscar Certificados onde presenca_confirmada=True
    return HttpResponse("Página de Meus Certificados")

# --- Rotas de Organizador ---

@login_required
@user_passes_test(is_organizador)
def criar_evento(request):
    """ 
    Formulário para criar um novo evento (rota: /eventos/novo/).
    Aplica validações de data e banner (implementadas no forms.py futuro).
    """
    return HttpResponse("Página de Criação de Evento")

@login_required
@user_passes_test(is_organizador)
def editar_evento(request, evento_id):
    """ 
    Formulário para editar um evento existente (rota: /eventos/editar/<id>/).
    """
    return HttpResponse(f"Página de Edição do Evento ID: {evento_id}")

@login_required
@user_passes_test(is_organizador)
def listar_eventos_organizador(request):
    """ 
    Lista de eventos gerenciados pelo organizador (rota: /eventos/gerenciar/).
    """
    return HttpResponse("Página de Gerenciamento de Eventos")

@login_required
@user_passes_test(is_organizador)
def lista_inscritos(request, evento_id):
    """ 
    Lista de participantes inscritos em um evento (rota: /evento/<id>/inscritos/). 
    Permite ao Organizador confirmar presença.
    """
    # Lógica futura: Buscar todas as Inscrições para o Evento.
    return HttpResponse(f"Lista de Inscritos para o Evento ID: {evento_id}")

@login_required
@user_passes_test(is_organizador)
def emitir_certificados(request, evento_id):
    """ 
    Gera certificados para o evento (rota: /evento/<id>/emitir_certificados/).
    Apenas para inscritos com presença_confirmada=True.
    """
    # Lógica futura: Disparar a automação de emissão de certificados.
    return HttpResponse(f"Processando Emissão de Certificados para o Evento ID: {evento_id}")
    
@login_required
@user_passes_test(is_organizador)
def registros_auditoria(request):
    """ 
    Tela para consultar logs de auditoria (rota: /auditoria/). 
    Requer acesso ao sistema de logs (futuramente).
    """
    return HttpResponse("Página de Registros de Auditoria (Logs)")