from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponseRedirect

def loading(request):
    return render(request, 'loading.html')

def index(request):
    return render(request, 'index.html')

def botellas(request):
    return render(request, 'botellas.html')

def lamparas(request):
    return render(request, 'lamparas.html')

def llaveros(request):
    return render(request, 'llaveros.html')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')

        if not user or not password:
            messages.error(request, 'Por favor completa todos los campos.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def peluches(request):
    return render(request, 'peluches.html')

def pines(request):
    return render(request, 'pines.html')

def productos(request):
    return render(request, 'productos.html')

def registro(request):
    return render(request, 'registro.html')

def termos(request):
    return render(request, 'termos.html')