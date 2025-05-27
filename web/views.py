from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import check_password, make_password
import re

# Vistas generales
def loading(request):
    return render(request, 'loading.html')

def index(request):
    return render(request, 'index.html')

def productos(request):
    return render(request, 'productos.html')

def carrito(request):
    return render(request, 'carrito.html')

# Validaciones
def validar_rut(rut):
    rut = rut.replace('.', '').lower().replace('-', '')
    if not re.match(r'^\d{7,8}[k0-9]$', rut):
        return False
    cuerpo = rut[:-1]
    dv = rut[-1]
    suma = sum(int(d) * (2 + i % 6) for i, d in enumerate(reversed(cuerpo)))
    resto = suma % 11
    digito = 'k' if 11 - resto == 10 else str(11 - resto)
    return digito == dv.lower()

def validar_contrasenna(contrasenna):
    if len(contrasenna) < 9:
        return "La contraseña debe tener al menos 9 caracteres."
    if not re.search(r'[A-Z]', contrasenna):
        return "Debe contener al menos una letra mayúscula."
    if not re.search(r'\d', contrasenna):
        return "Debe contener al menos un número."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', contrasenna):
        return "Debe contener al menos un carácter especial (!@#$%^&*(), etc.)."
    return None

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 9 and telefono.startswith('9')

# Registro
def registro(request):
    context = {
        'nombre': '',
        'apellido': '',
        'id_usuario': '',
        'correo': '',
        'direccion': '',
        'telefono': ''
    }

    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        contrasenna = request.POST.get('contrasenna')
        confirm_contrasenna = request.POST.get('confirm-contra')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        context.update({
            'nombre': nombre,
            'apellido': apellido,
            'id_usuario': id_usuario,
            'correo': correo,
            'direccion': direccion,
            'telefono': telefono
        })

        if not all([id_usuario, nombre, apellido, correo, contrasenna, confirm_contrasenna, direccion, telefono]):
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'registro.html', context)

        if not validar_telefono(telefono):
            messages.error(request, 'El teléfono debe tener 9 dígitos y comenzar con 9.')
            return render(request, 'registro.html', context)

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'registro.html', context)

        if Usuario.objects.filter(id_usuario=id_usuario).exists():
            messages.error(request, 'El RUT ya está registrado.')
            return render(request, 'registro.html', context)

        if not validar_rut(id_usuario):
            messages.error(request, 'El RUT ingresado no es válido. Ejemplo: 12345678-9')
            return render(request, 'registro.html', context)

        error_pass = validar_contrasenna(contrasenna)
        if error_pass:
            messages.error(request, error_pass)
            return render(request, 'registro.html', context)

        if contrasenna != confirm_contrasenna:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html', context)

        try:
            usuario = Usuario(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasenna=contrasenna,
                direccion=direccion,
                telefono=telefono,
                rol='cliente'
            )
            usuario.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar el usuario: {e}')
            return render(request, 'registro.html', context)

    return render(request, 'registro.html', context)

# Login
def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenna = request.POST.get('contrasenna')

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo electrónico incorrecto.')
            return redirect('login')

        if not check_password(contrasenna, usuario.contrasenna):
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login')

        request.session['usuario_id'] = usuario.id_usuario
        messages.success(request, 'Inicio de sesión exitoso.')
        return redirect('index')

    return render(request, 'login.html')
