from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Producto, Stock, AlertaStock
from django.shortcuts import get_object_or_404

def productos(request):
    return render(request, 'dj/productos.html')
# Vistas generales
def loading(request):
    return render(request, 'loading.html')

def index(request):
    return render(request, 'index.html')

def productos(request):
    productos = Producto.objects.all()
    print(f"Consulta SQL generada: {Producto.objects.all().query}")  # Ver consulta SQL
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




@require_POST
def agregar_al_carrito(request, id_producto):
    try:
        # Obtener el producto o devolver 404 si no existe
        producto = get_object_or_404(Producto, pk=id_producto)

        # Obtener el carrito de la sesión o iniciar uno vacío
        carrito = request.session.get('carrito', [])

        # Buscar si el producto ya está en el carrito para aumentar cantidad
        for item in carrito:
            if item['id'] == producto.id_producto:
                item['cantidad'] += 1
                break
        else:
            # Si no está, agregarlo como nuevo con cantidad 1
            carrito.append({
                'id': producto.id_producto,
                'nombre': producto.nombre,
                'precio': float(producto.precio or 0),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else ''
            })

        # Guardar el carrito actualizado en la sesión
        request.session['carrito'] = carrito
        request.session.modified = True

        return JsonResponse({'success': True})
    
    except Producto.DoesNotExist:
        # En caso que no se encuentre el producto
        return JsonResponse({'success': False, 'error': 'Producto no encontrado.'}, status=404)
    
    except Exception as e:
        # Cualquier otro error inesperado
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def obtener_carrito(request):
    carrito = request.session.get('carrito', [])
    return JsonResponse({'carrito': carrito})

def ver_carrito(request):
    # Obtener el carrito de la sesión, por defecto una lista vacía
    carrito = request.session.get('carrito', [])

    # Validar que sea una lista y tenga items con estructura correcta
    if not isinstance(carrito, list):
        carrito = []

    try:
        subtotal = sum(float(item['precio']) * int(item['cantidad']) for item in carrito if
                       isinstance(item, dict) and 'precio' in item and 'cantidad' in item)
    except (TypeError, ValueError):
        subtotal = 0

    context = {
        'carrito': carrito,
        'subtotal': subtotal,
    }

    return render(request, 'carrito.html', context)

#-------------------------------------------------------------------------------------#

def nosotros(request):
    return render(request, 'nosotros.html')

def informes_stock(request):
    productos = Producto.objects.all()
    alertas = []

    for producto in productos:
        stock_obj = producto.stock_set.first()

        if stock_obj:
            stock_actual = int(stock_obj.cantidad)  # Asegura que sea un entero
            ubicacion = stock_obj.ubicacion_detalle

            # Actualizar o crear AlertaStock
            alerta, created = AlertaStock.objects.get_or_create(
                producto=producto,
                defaults={
                    'stock_actual': stock_actual,
                    'ubicacion_detalle': ubicacion
                }
            )

            if not created:
                alerta.stock_actual = stock_actual
                alerta.save()

            print(f"Producto: {producto.nombre}, Stock Actual: {stock_actual}")  # Depuración
            alertas.append(alerta)

    return render(request, 'informes_stock.html', {'alertas': alertas})

def actualizar_stock(request, alerta_id):
    if request.method == 'POST':
        try:
            cantidad_a_agregar = int(request.POST.get('cantidad'))
            alerta = AlertaStock.objects.get_or_create(producto_id=Producto.id_producto)
            stock = alerta.producto.stock_set.first()

            if stock:
                stock.cantidad += cantidad_a_agregar
                stock.save()
                alerta.stock_actual = stock.cantidad
                alerta.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'No hay stock asociado.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})