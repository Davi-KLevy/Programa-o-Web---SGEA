# sgea_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# ------------------------------------
# 1. Modelo de Usuário Customizado
# Reflete as alterações na tabela Usuário do diagrama.
# O Django já inclui os campos 'username', 'password' e 'email'.
# Faremos o 'email' ser obrigatório para a autenticação.
# ------------------------------------

class UsuarioCustom(AbstractUser):
    # Campos que já existem no AbstractUser: username, email (herdado), password, first_name, last_name, is_staff, etc.

    # Definindo 'email' como campo de login principal
    # [cite_start]Usaremos o campo 'username' para o login conforme o requisito original [cite: 9]
    # mas garantimos que o 'email' exista e seja obrigatório (NOT NULL) como no diagrama.
    email = models.EmailField(unique=True, null=False, blank=False)

    # Campos Adicionais (conforme o diagrama e requisito do projeto)
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    instituicao_ensino = models.CharField(max_length=50, null=True, blank=True) # Requisito: obrigatório para alunos/professores. O Diagrama o manteve.
    perfil = models.CharField(max_length=50, choices=[
        ('Aluno', 'Aluno'),
        ('Professor', 'Professor'),
        ('Organizador', 'Organizador'),
    ])

    # O campo 'login' do diagrama anterior é tipicamente o 'username' ou 'email' no Django.
    # Vamos manter 'username' para fins de login (ou você pode trocar USERNAME_FIELD para 'email').

    def __str__(self):
        return self.nome

# ------------------------------------
# 2. Modelo de Evento
# Reflete a adição do campo 'nome char(50) NOT NULL'.
# ------------------------------------

class Evento(models.Model):
    organizador = models.ForeignKey(UsuarioCustom, on_delete=models.CASCADE, related_name='eventos_organizados')
    nome = models.CharField(max_length=50, null=False, blank=False, default='Novo Evento') # NOVO CAMPO
    tipo_evento = models.CharField(max_length=50)
    data_inicial = models.DateField()
    data_final = models.DateField()
    horario = models.CharField(max_length=50)
    local = models.CharField(max_length=50)
    quantidade_participantes = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.tipo_evento}"

    class Meta:
        verbose_name_plural = "Eventos"

# ------------------------------------
# 3. Modelos de Inscrição e Certificado
# Precisam referenciar o novo modelo de usuário customizado (UsuarioCustom)
# ------------------------------------

class Inscricao(models.Model):
    usuario = models.ForeignKey(UsuarioCustom, on_delete=models.CASCADE, related_name='inscricoes') # Mudança de settings.AUTH_USER_MODEL para UsuarioCustom
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name_plural = "Inscrições"

class Certificado(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, unique=True, related_name='certificado')
    data_emissao = models.DateField()
    texto_certificado = models.CharField(max_length=50)
    status_emissao = models.CharField(max_length=50, choices=[
        ('Pendente', 'Pendente'),
        ('Emitido', 'Emitido'),
    ])

    def __str__(self):
        return f"Certificado para {self.inscricao.usuario.nome}"
    
    class Meta:
        verbose_name_plural = "Certificados"