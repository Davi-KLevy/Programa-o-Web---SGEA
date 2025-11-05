from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.utils import timezone
from .forms import * 
from .models import *
# Importe o forms.py que criamos no passo anterior.

# --- Funções Auxiliares de Permissão ---

def is_organizador(user):
    """ Verifica se o usuário é um organizador e está ativo/autenticado. """
    return user.is_authenticated and user.perfil == 'Organizador'

def is_professor_or_organizador(user):
    """ Verifica se o usuário é um professor ou organizador. """
    return user.is_authenticated and user.perfil in ['Professor', 'Organizador']

def is_aluno_or_professor(user):
    """ Verifica se o usuário é um Aluno ou Professor e está ativo/autenticado. """
    return user.is_authenticated and user.perfil in ['Aluno', 'Professor']

# --- Rotas Públicas ---

def lista_eventos(request):
    """
    Exibe a lista de todos os eventos ativos. 
    Se o usuário for Organizador (logado), é redirecionado para o dashboard.
    """
    if request.user.is_authenticated and request.user.perfil == 'Organizador':
        # Bloqueia o Organizador, pois ele só deve usar o dashboard
        return redirect('dashboard') 
        
    hoje = timezone.now().date()
    
    # Busca eventos que a data final seja HOJE ou no futuro
    eventos_ativos = Evento.objects.filter(
        data_final__gte=hoje
    ).order_by('data_inicial') # Ordena pelo mais próximo
    
    context = {
        'eventos': eventos_ativos,
        'title': 'Eventos Acadêmicos Disponíveis'
    }
    return render(request, 'lista_eventos.html', context)

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
@login_required
def dashboard(request):
    """ 
    Dashboard após o login (rota: /dashboard/). 
    Se Organizador, lista seus eventos.
    """
    context = {}
    
    if is_organizador(request.user):
        # Se for Organizador, busca e lista seus eventos
        eventos_organizados = Evento.objects.filter(
            organizador=request.user
        ).order_by('data_inicial')
        
        context['eventos_organizados'] = eventos_organizados
        
    # Lógica futura: Minhas Inscrições (para Aluno/Professor)
    # if request.user.perfil in ['Aluno', 'Professor']:
    #     minhas_inscricoes = Inscricao.objects.filter(usuario=request.user)
    #     context['minhas_inscricoes'] = minhas_inscricoes
        
    return render(request, 'dashboard.html', context)

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
@user_passes_test(is_aluno_or_professor) # Apenas Aluno ou Professor
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
    Aplica validações de data e banner (implementadas no forms.py).
    """
    if request.method == 'POST':
        form = FormularioEvento(request.POST, request.FILES) # Usa request.FILES para o banner
        if form.is_valid():
            evento = form.save(commit=False)
            
            # Define o organizador responsável como o usuário logado [cite: 93]
            evento.organizador = request.user 
            evento.save()
            
            # Redireciona para a lista de gerenciamento de eventos
            return redirect('dashboard') 
    else:
        form = FormularioEvento()
        
    return render(request, 'criar_evento.html', {'form': form, 'title': 'Criar Novo Evento'})

@login_required
@user_passes_test(is_organizador)
def editar_evento(request, evento_id):
    """ 
    Formulário para editar um evento existente.
    """
    # 1. Busca o evento ou retorna 404
    evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
    
    # 2. Processa a submissão
    if request.method == 'POST':
        # Instancia o formulário com os dados POST, arquivos e a instância do objeto
        form = FormularioEvento(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            # A view de criação não precisa definir 'organizador' aqui, pois ele já está
            # na instância 'evento' e o formulário o mantém.
            form.save()
            return redirect('dashboard') 
    else:
        # 3. Exibe o formulário preenchido (GET)
        form = FormularioEvento(instance=evento)
        
    context = {
        'form': form, 
        'title': f'Editar Evento: {evento.nome}',
        'evento_id': evento.id
    }
    # O template 'editar_evento.html' será o próximo a ser criado
    return render(request, 'editar_evento.html', context)

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