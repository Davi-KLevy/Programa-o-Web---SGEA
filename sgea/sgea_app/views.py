from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.utils import timezone
from .forms import * 
from .models import *
from django.contrib.auth import get_user_model
from .tokens import token_ativacao
from django.contrib.auth.tokens import default_token_generator

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

# ADICIONADO: View home para a página inicial
def home(request):
    """Página inicial do sistema"""
    return render(request, 'home.html')

# RENOMEADO de lista_eventos para eventos_lista (para combinar com as URLs)
def eventos_lista(request):
    """
    Exibe a lista de eventos que ainda não começaram e que o usuário (se logado)
    ainda não se inscreveu. Redireciona Organizadores para o dashboard.
    """
    hoje = timezone.now().date()
    
    # Filtro base: Apenas eventos que ainda não começaram
    eventos_queryset = Evento.objects.filter(
        data_inicial__gt=hoje
    ).order_by('data_inicial')
    
    if request.user.is_authenticated:
        # 1. Restrição para Organizador
        if request.user.perfil == 'Organizador':
            return redirect('sgea_app:dashboard')  # AJUSTADO: namespace da URL
        
        # 2. Filtragem para Aluno/Professor (excluir inscritos)
        elif request.user.perfil in ['Aluno', 'Professor']:
            
            # Pega os IDs dos eventos em que o usuário está inscrito
            eventos_inscritos_ids = Inscricao.objects.filter(
                usuario=request.user
            ).values_list('evento__id', flat=True)
            
            # Exclui da listagem todos os eventos que o usuário já está inscrito
            eventos_disponiveis = eventos_queryset.exclude(
                id__in=eventos_inscritos_ids
            )
            
    else:
        # 3. Usuário Não Logado (vê todos os eventos futuros)
        eventos_disponiveis = eventos_queryset
            
    context = {
        'eventos': eventos_disponiveis,
        'title': 'Eventos Acadêmicos Disponíveis'
    }
    return render(request, 'eventos/lista.html', context)  # AJUSTADO: caminho do template

# RENOMEADO de detalhe_evento para evento_detalhes
def evento_detalhes(request, evento_id):
    """ 
    Exibe os detalhes de um evento específico (rota: /evento/<id>/). 
    Inclui botão de inscrição se o usuário for Aluno/Professor.
    """
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'eventos/detalhes.html', {'evento': evento})

# RENOMEADO de cadastro_usuario para usuario_cadastro
def usuario_cadastro(request):
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
            # até a confirmação por e-mail.
            novo_usuario.is_active = False
            novo_usuario.save()

            from .utils import enviar_email_confirmacao
            enviar_email_confirmacao(novo_usuario, request)

            messages.success(request, "Cadastro realizado! Verifique seu e-mail para ativar sua conta.")
            return redirect('sgea_app:login')  # AJUSTADO: namespace
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = CadastroUsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form':form})  # AJUSTADO: caminho


Usuario = get_user_model()

def confirmar_email(request, uid, token):
    """
    Ativa o usuário após clicar no link enviado por e-mail.
    """
    try:
        usuario = Usuario.objects.get(pk=uid)
    except Usuario.DoesNotExist:
        return HttpResponse("Usuário inválido.", status=400)

    if token_ativacao.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        return HttpResponse(
            "E-mail confirmado com sucesso! Sua conta foi ativada.", 
            status=200
        )
    else:
        return HttpResponse("Link inválido ou expirado.", status=400)
    
# ADICIONADO: Views de login/logout básicas
def usuario_login(request):
    """Página de login"""
    # Aqui você pode implementar a lógica de login personalizada
    # ou usar a view do Django contrib.auth
    return render(request, 'usuarios/login.html')

def usuario_logout(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso!')
    return redirect('sgea_app:login')

@login_required
def usuario_perfil(request):
    """Perfil do usuário"""
    return render(request, 'usuarios/perfil.html')

@login_required
def dashboard(request):
    """ 
    Dashboard após o login (rota: /dashboard/). 
    Se Organizador, lista seus eventos.
    Se Aluno/Professor, lista suas inscrições.
    """
    context = {}
    usuario = request.user
    
    if is_organizador(usuario):
        # Se for Organizador
        eventos_organizados = Evento.objects.filter(
            organizador=usuario
        ).order_by('data_inicial')
        
        context['eventos_organizados'] = eventos_organizados
        
    elif usuario.perfil in ['Aluno', 'Professor']:
        # Se for Aluno ou Professor
        
        # Filtra as inscrições do usuário e pré-busca os dados do evento
        minhas_inscricoes = Inscricao.objects.filter(
            usuario=usuario
        ).select_related('evento').order_by('evento__data_inicial')
        
        context['minhas_inscricoes'] = minhas_inscricoes
        
    return render(request, 'dashboard.html', context)

# RENOMEADO de inscrever_evento para inscricao_criar
@login_required
def inscricao_criar(request, evento_id):
    """ 
    Processa a inscrição de um usuário (Aluno/Professor) em um evento.
    """
    evento = get_object_or_404(Evento, pk=evento_id)
    usuario = request.user
    hoje = timezone.now().date()
    
    # 1. Restrição de Acesso (Apenas Aluno/Professor) 
    if usuario.perfil not in ['Aluno', 'Professor']:
        messages.error(request, "Apenas usuários com perfil Aluno ou Professor podem se inscrever em eventos.")
        return redirect('sgea_app:home')  # AJUSTADO: namespace
        
    # 2. Verificar se o evento já começou (só permite inscrição em eventos futuros)
    if evento.data_inicial < hoje:
        messages.error(request, f"Não é possível se inscrever no evento '{evento.nome}', pois ele já começou ou terminou.")
        return redirect('sgea_app:home')

    # 3. Verificar Inscrição Duplicada
    if Inscricao.objects.filter(usuario=usuario, evento=evento).exists():
        messages.warning(request, f"Você já está inscrito no evento '{evento.nome}'.")
        return redirect('sgea_app:home') 

    # 4. Verificar Limite de Vagas
    total_inscritos = Inscricao.objects.filter(evento=evento).count()
    
    if total_inscritos >= evento.quantidade_participantes:
        messages.error(request, f"O evento '{evento.nome}' atingiu o limite de vagas.")
        return redirect('sgea_app:home')
    
    try:
        # 5. Criar Inscrição
        Inscricao.objects.create(usuario=usuario, evento=evento)
        messages.success(request, f"Inscrição no evento '{evento.nome}' realizada com sucesso!")
        
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao processar sua inscrição. Tente novamente.")
        # Logar o erro 'e' aqui para depuração
        
    return redirect('sgea_app:home')

@login_required
def desinscrever_evento(request, evento_id):
    """ 
    Permite ao usuário (Aluno/Professor) cancelar sua inscrição em um evento futuro.
    """
    evento = get_object_or_404(Evento, pk=evento_id)
    usuario = request.user
    hoje = timezone.now().date()
    
    # 1. Busca a inscrição
    inscricao = get_object_or_404(Inscricao, usuario=usuario, evento=evento)
    
    # 2. Verifica se o evento já começou (só permite cancelamento em eventos futuros)
    if evento.data_inicial < hoje:
        messages.error(request, f"Não é possível cancelar a inscrição, pois o evento '{evento.nome}' já começou ou terminou.")
        return redirect('sgea_app:dashboard')

    # 3. Processa a desinscrição (usando POST, que é mais seguro)
    if request.method == 'POST':
        try:
            inscricao.delete()
            messages.success(request, f"Inscrição no evento '{evento.nome}' cancelada com sucesso.")
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao cancelar sua inscrição.")
        
    # Redireciona para o dashboard, onde a lista de inscrições será atualizada
    return redirect('sgea_app:dashboard')

# RENOMEADO de meus_certificados para minhas_inscricoes
@login_required
@user_passes_test(is_aluno_or_professor) # Apenas Aluno ou Professor
def minhas_inscricoes(request):
    """ 
    Lista as inscrições do usuário.
    """
    inscricoes = Inscricao.objects.filter(
        usuario=request.user
    ).select_related('evento').order_by('evento__data_inicial')
    
    return render(request, 'inscricoes/minhas_inscricoes.html', {'inscricoes': inscricoes})

@login_required
@user_passes_test(is_aluno_or_professor)
def meus_certificados(request):
    """ 
    Lista os certificados do usuário (rota: /meus_certificados/).
    Permitido para Alunos e Professores.
    """
    # Lógica futura: Buscar Certificados onde presenca_confirmada=True
    return HttpResponse("Página de Meus Certificados")

# --- Rotas de Organizador ---

# RENOMEADO de criar_evento para evento_cadastro
@login_required
@user_passes_test(is_organizador)
def evento_cadastro(request):
    """ 
    Formulário para criar um novo evento (rota: /eventos/novo/).
    Aplica validações de data e banner (implementadas no forms.py).
    """
    if request.method == 'POST':
        form = FormularioEvento(request.POST, request.FILES) # Usa request.FILES para o banner
        if form.is_valid():
            evento = form.save(commit=False)
            
            # Define o organizador responsável como o usuário logado 
            evento.organizador = request.user 
            evento.save()
            
            # Redireciona para a lista de gerenciamento de eventos
            return redirect('sgea_app:dashboard')  # AJUSTADO: namespace
    else:
        form = FormularioEvento()
        
    return render(request, 'eventos/cadastro.html', {'form': form, 'title': 'Criar Novo Evento'})

# RENOMEADO de editar_evento para evento_editar
@login_required
@user_passes_test(is_organizador)
def evento_editar(request, evento_id):
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
            form.save()
            return redirect('sgea_app:dashboard')  # AJUSTADO: namespace
    else:
        # 3. Exibe o formulário preenchido (GET)
        form = FormularioEvento(instance=evento)
        
    context = {
        'form': form, 
        'title': f'Editar Evento: {evento.nome}',
        'evento_id': evento.id
    }
    return render(request, 'eventos/editar.html', context)

# ADICIONADO: View para deletar evento
@login_required
@user_passes_test(is_organizador)
def evento_deletar(request, evento_id):
    """Deleta um evento"""
    evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
    
    if request.method == 'POST':
        evento.delete()
        messages.success(request, f"Evento '{evento.nome}' deletado com sucesso!")
        return redirect('sgea_app:dashboard')
    
    return render(request, 'eventos/confirmar_delete.html', {'evento': evento})

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

# RENOMEADO de registros_auditoria para auditoria_logs
@login_required
@user_passes_test(is_organizador)
def auditoria_logs(request):
    """ 
    Tela para consultar logs de auditoria (rota: /auditoria/). 
    Requer acesso ao sistema de logs (futuramente).
    """
    logs = []  # Temporariamente vazio
    context = {
        'logs': logs,
        'total_registros': 0,
        'registros_hoje': 0,
        'usuarios_ativos': 0,
        'acoes_criticas': 0,
        'usuarios': [],  # Lista de usuários para o filtro
    }
    return render(request, 'auditoria/logs.html', context)