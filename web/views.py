from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from .models import producto


def productos(request):
    return render(request, 'dj/productos.html')
# Vistas generales
def loading(request):
    return render(request, 'loading.html')

def index(request):
    return render(request, 'index.html')

def productos(request):
    productos = producto.objects.all()
    print(f"Consulta SQL generada: {producto.objects.all().query}")  # Ver consulta SQL
    print(f"Todos los productos: {productos}")  # Depuración

    peluches = [p for p in productos if 1000 <= p.id_producto < 2000]
    botellas = [p for p in productos if 2000 <= p.id_producto < 3000]
    termos = [p for p in productos if 3000 <= p.id_producto < 4000]
    pines = [p for p in productos if 4000 <= p.id_producto < 5000]
    llaveros = [p for p in productos if 5000 <= p.id_producto < 6000]
    lamparas = [p for p in productos if 6000 <= p.id_producto < 7000]

    print(f"Peluches: {peluches}")  # Depuración
    print(f"Botellas: {botellas}")  # Depuración
    print(f"Termos: {termos}")  # Depuración
    print(f"Pines: {pines}")  # Depuración
    print(f"Llaveros: {llaveros}")  # Depuración
    print(f"Lámparas: {lamparas}")  # Depuración

    return render(request, 'productos.html', {
        'peluches': peluches,
        'botellas': botellas,
        'termos': termos,
        'pines': pines,
        'llaveros': llaveros,
        'lamparas': lamparas
    })


def carrito(request):
    return render(request, 'carrito.html')

# Validaciones
def validar_contrasenna(contrasenna):
    if len(contrasenna) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r'[A-Z]', contrasenna):
        return "Debe contener al menos una letra mayúscula."
    if not re.search(r'\d', contrasenna):
        return "Debe contener al menos un número."
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
        id_usuario = request.POST.get('id_usuario', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasenna = request.POST.get('contrasenna', '').strip()
        confirm_contrasenna = request.POST.get('confirm-contra', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        context.update({
            'nombre': nombre,
            'apellido': apellido,
            'id_usuario': id_usuario,
            'correo': correo,
            'direccion': direccion,
            'telefono': telefono
        })

        # Validación de campos vacíos
        if not all([id_usuario, nombre, apellido, correo, contrasenna, confirm_contrasenna, direccion, telefono]):
            messages.error(request, 'Por favor, completa todos los campos.')
            return render(request, 'registro.html', context)

        # Validar formato de email
        try:
            validate_email(correo)
        except ValidationError:
            messages.error(request, 'El correo electrónico no es válido.')
            return render(request, 'registro.html', context)

        # Validar teléfono
        if not validar_telefono(telefono):
            messages.error(request, 'El teléfono debe tener 9 dígitos y comenzar con 9.')
            return render(request, 'registro.html', context)

        # Validar si el correo ya existe
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Correo ya existente')
            return render(request, 'registro.html', context)

        # Validar si el RUT ya existe
        if Usuario.objects.filter(id_usuario=id_usuario).exists():
            messages.error(request, 'Error al ingresar RUT')
            return render(request, 'registro.html', context)

        # Validar contraseña segura
        error_pass = validar_contrasenna(contrasenna)
        if error_pass:
            messages.error(request, error_pass)
            return render(request, 'registro.html', context)

        # Validar coincidencia de contraseñas
        if contrasenna != confirm_contrasenna:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html', context)


            


        # Guardar usuario
        try:
            usuario = Usuario(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasenna=make_password(contrasenna),
                direccion=direccion,
                telefono=telefono,
                rol='cliente'
            )
            usuario.save()
            messages.success(request, 'Registro exitoso. ¡Ahora puedes iniciar sesión!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar el usuario: {e}')
            return render(request, 'registro.html', context)

    return render(request, 'registro.html', context)

# Login
def login(request):
    # Redirigir si el usuario ya está logueado
    if 'usuario_id' in request.session:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Validar que ambos campos estén llenos
        if not email or not password:
            messages.error(request, 'Por favor ingresa correo y contraseña.')
            return render(request, 'login.html', {'email': email})

        try:
            usuario = Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'login.html', {'email': email})

        # Verificar contraseña
        if not check_password(password, usuario.contrasenna):
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'login.html', {'email': email})

        # Iniciar sesión
        request.session['usuario_id'] = usuario.id_usuario
        messages.success(request, 'Inicio de sesión exitoso.')
        return redirect('index')
    
    return render(request, 'login.html')

def validar_rut_chileno(rut):
    """
    Valida un RUT chileno incluyendo el dígito verificador.
    Formato esperado: 12345678-9 o 12.345.678-9
    """
    rut = rut.replace('.', '').replace('-', '').upper()
    if len(rut) < 2:
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    # Validar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        return False

    # Calcular dígito verificador
    suma = 0
    factor = 2
    for c in reversed(cuerpo):
        suma += int(c) * factor
        factor = 2 if factor == 7 else factor + 1

    dv_real = str(11 - (suma % 11))
    if dv_real == "10":
        dv_real = "K"
    elif dv_real == "11":
        dv_real = "0"

    return dv == dv_real


@login_required
def registro_admin(request):
    if request.user.rol != 'admin':
        messages.error(request, "Acceso denegado.")
        return redirect('index')

    context = {
        'nombre': '',
        'apellido': '',
        'id_usuario': '',
        'correo': '',
        'direccion': '',
        'telefono': ''
    }

    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasenna = request.POST.get('contrasenna', '').strip()
        confirm_contrasenna = request.POST.get('confirm-contra', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        rol = request.POST.get('rol', 'cliente')  # Obtiene el rol seleccionado

        context.update({
            'nombre': nombre,
            'apellido': apellido,
            'id_usuario': id_usuario,
            'correo': correo,
            'direccion': direccion,
            'telefono': telefono
        })

        # Validación de campos vacíos
        if not all([id_usuario, nombre, apellido, correo, contrasenna, confirm_contrasenna, direccion, telefono]):
            messages.error(request, 'Por favor completa todos los campos.')
            return render(request, 'registro_admin.html', context)

        # Validar formato de email
        try:
            validate_email(correo)
        except ValidationError:
            messages.error(request, 'Correo electrónico inválido.')
            return render(request, 'registro_admin.html', context)

        # Validar teléfono chileno
        if len(telefono) != 9 or not telefono.isdigit() or not telefono.startswith('9'):
            messages.error(request, 'Teléfono inválido (debe tener 9 dígitos y comenzar con 9).')
            return render(request, 'registro_admin.html', context)

        # Validar si el correo o rut ya existen
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return render(request, 'registro_admin.html', context)

        if Usuario.objects.filter(id_usuario=id_usuario).exists():
            messages.error(request, 'El RUT ya está registrado.')
            return render(request, 'registro_admin.html', context)

        # Validar contraseña segura
        error_pass = validar_contrasenna(contrasenna)
        if error_pass:
            messages.error(request, error_pass)
            return render(request, 'registro_admin.html', context)

        # Validar coincidencia de contraseñas
        if contrasenna != confirm_contrasenna:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro_admin.html', context)

        # Guardar usuario con rol asignado por el admin
        try:
            usuario = Usuario(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasenna=make_password(contrasenna),
                direccion=direccion,
                telefono=telefono,
                rol=rol
            )
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('registro_admin')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar el usuario: {e}')
            return render(request, 'registro_admin.html', context)

    return render(request, 'registro_admin.html', context)


def index(request):
    # Inicializa el carrito si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    return render(request, 'index.html')


@csrf_protect
def agregar_al_carrito(request, id_producto):
    try:
        prod = producto.objects.get(id_producto=id_producto)

        carrito = request.session.get('carrito', [])

        encontrado = False
        for item in carrito:
            if item['id'] == id_producto:
                item['cantidad'] += 1
                encontrado = True
                break

        if not encontrado:
            carrito.append({
                'id': prod.id_producto,
                'nombre': prod.nombre,
                'imagen': prod.imagen,
                'precio': float(prod.precio),
                'cantidad': 1
            })

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'success': True})
    except producto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
    
def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)

    context = {
        'carrito': carrito,
        'subtotal': subtotal,
    }
    return render(request, 'carrito.html', context)

def carrito_view(request):
    carrito = request.session.get('carrito', [])
    # Pasar carrito al template
    context = {'carrito': carrito}
    return render(request, 'carrito.html', context)

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
        request.session.modified = True

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

def obtener_carrito(request):
    carrito = request.session.get('carrito', [])
    return JsonResponse({'carrito': carrito})

@csrf_protect
def aumentar_cantidad(request, id_producto):
    try:
        carrito = request.session.get('carrito', [])

        for item in carrito:
            if item['id'] == id_producto:
                item['cantidad'] += 1
                break

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_protect
def disminuir_cantidad(request, id_producto):
    try:
        carrito = request.session.get('carrito', [])

        for item in carrito:
            if item['id'] == id_producto:
                if item['cantidad'] > 1:
                    item['cantidad'] -= 1
                else:
                    # Si la cantidad es 1, elimina el producto
                    carrito = [i for i in carrito if i['id'] != id_producto]
                break

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_protect
def eliminar_producto(request, id_producto):
    try:
        carrito = request.session.get('carrito', [])

        carrito = [item for item in carrito if item['id'] != id_producto]

        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
# Función auxiliar para calcular respuesta JSON
def calcular_respuesta_carrito(carrito):
    cart_count = sum(item['cantidad'] for item in carrito)
    subtotal = sum(item['cantidad'] * item.get('precio', 0) for item in carrito)
    return {
        'success': True,
        'cart_count': cart_count,
        'subtotal': subtotal,
        'carrito': carrito
    }
def obtener_cantidad_carrito(request):
    carrito = request.session.get('carrito', [])
    total = sum(item['cantidad'] for item in carrito)
    return JsonResponse({'count': total})

def nosotros(request):
    return render(request, 'nosotros.html')

