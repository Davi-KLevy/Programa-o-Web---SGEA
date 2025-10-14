# eventos/models.py

from django.db import models
from django.conf import settings # Para referenciar o modelo de usuário do Django

# NOTA: Para o modelo Usuário, você deve customizar o modelo de autenticação do Django (AUTH_USER_MODEL)
# para incluir campos como telefone, instituicao_ensino e perfil, conforme o requisito.
# Para esta etapa, vamos usar o modelo de usuário padrão (settings.AUTH_USER_MODEL).

class Evento(models.Model):
    # organizador_id é uma Chave Estrangeira para o Usuário
    organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventos_organizados')
    tipo_evento = models.CharField(max_length=50) # Ex: Palestra, Seminário, Minicurso
    data_inicial = models.DateField() #
    data_final = models.DateField() #
    horario = models.CharField(max_length=50) #
    local = models.CharField(max_length=50) #
    quantidade_participantes = models.IntegerField() #

    def __str__(self):
        return f"{self.tipo_evento} em {self.local} ({self.data_inicial})"
    
    class Meta:
        verbose_name_plural = "Eventos"

class Inscricao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscricoes')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')

    class Meta:
        unique_together = ('usuario', 'evento') # Garante 1 inscrição por usuário/evento
        verbose_name_plural = "Inscrições"

# O modelo Certificado também seria criado aqui, mas o foco é a tela inicial.
# class Certificado(models.Model): ...