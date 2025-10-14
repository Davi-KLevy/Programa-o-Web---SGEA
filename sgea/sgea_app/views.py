
from django.shortcuts import render
from .models import Evento

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('data_inicial') # Busca todos os eventos
    context = {'eventos': eventos}
    return render(request, 'sgea_app/lista_eventos.html', context)