from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def principal(request):
    return render(request, 'sgea_app/principal.html')

def login(request):
    return render(request, 'sgea_app/login.html')

def cadastro(request):
    return render(request, 'sgea_app/cadastro.html')

def participante(request):
    return render(request, 'sgea_app/participante.html')

def organizador(request):
    return render(request, 'sgea_app/organizador.html')