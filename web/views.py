from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Vistas generales
def loading(request):
    return render(request, 'loading.html')

def login(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

def index(request):
    return render(request, 'index.html')

def productos(request):
    return render(request, 'productos.html')

def carrito(request):
    return render(request, 'carrito.html')

def index(request):
    return render(request, 'index.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def agregar_al_carrito(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')

        nuevo_producto = {
            "nombre": nombre,
            "precio": precio
        }

        carrito = request.session.get('carrito', [])
        carrito.append(nuevo_producto)
        request.session['carrito'] = carrito  # Guarda de nuevo en sesión

        return JsonResponse({
            "success": True,
            "cart_count": len(carrito)
        })

    return JsonResponse({"success": False}, status=400)

def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    
    # Calcula el total del carrito
    total = sum(int(producto['precio']) for producto in carrito)
    
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})


def eliminar_del_carrito(request):
    if request.method == "POST":
        nombre_producto = request.POST.get("nombre")
        carrito = request.session.get("carrito", [])

        # Filtrar y eliminar solo el primer coincidente
        for i, producto in enumerate(carrito):
            if producto["nombre"] == nombre_producto:
                carrito.pop(i)
                break

        request.session['carrito'] = carrito
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)