from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import authenticate, login
from .models import Producto, Stock, AlertaStock, Carrito
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from .models import Producto
from django.views.decorators.csrf import csrf_exempt





def productos(request):
    productos = Producto.objects.all()
    # ...tu lógica de categorías...
    cart_count = sum(item['cantidad'] for item in request.session.get('carrito', []))
    return render(request, 'productos.html', {
        'peluches': peluches,  # type: ignore
        'botellas': botellas, # type: ignore
        'termos': termos, # type: ignore
        'pines': pines, # type: ignore
        'llaveros': llaveros, # type: ignore
        'lamparas': lamparas, # type: ignore
        'cart_count': cart_count,
    })
# Vistas generales
def loading(request):
    return render(request, 'loading.html')

def index(request):
    # Filtrar productos destacados por ID
    destacados = Producto.objects.filter(id_producto__in=['1001', '1002', '1003', '1004', '1005', '1006'])
    
    context = {
        'productos': destacados,
    }
    return render(request, 'index.html', context)

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
    carrito = request.session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})
#@login_required
def pago(request):
    # Puedes pasar el carrito y el total si lo necesitas en la página de pago
    carrito = request.session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    return render(request, 'pago.html', {'carrito': carrito, 'total': total})
def pago_transferencia(request):
    mensaje = None
    if request.method == 'POST':
        comprobante = request.FILES.get('comprobante')
        # Descontar stock
        carrito = request.session.get('carrito', [])
        for item in carrito:
            try:
                producto = Producto.objects.get(id_producto=item['id'])
                producto.stock_set.first().cantidad -= item['cantidad']
                producto.stock_set.first().save()
            except Producto.DoesNotExist:
                pass
        # Limpiar el carrito
        request.session['carrito'] = []
        request.session.modified = True
        mensaje = "¡Pago recibido con éxito! Pronto confirmaremos tu pago."
        return redirect('pago_exito')  # Esto es correcto
    return render(request, 'pago_transferencia.html', {'mensaje': mensaje})

def pago_tarjeta(request):
    if request.method == 'POST':
        # Aquí puedes procesar los datos de la tarjeta (solo ejemplo, no real)
        # numero = request.POST.get('numero')
        # expira = request.POST.get('expira')
        # cvv = request.POST.get('cvv')
        # Procesa el pago o muestra mensaje de éxito
        return render(request, 'pago_exito.html')
    return render(request, 'pago_tarjeta.html')

def pago_exito(request):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        try:
            producto = Producto.objects.get(id_producto=item['id'])
            stock_obj = producto.stock_set.first()
            if stock_obj:
                # Convierte ambos a int para evitar problemas de tipo
                cantidad_actual = int(stock_obj.cantidad)
                cantidad_comprada = int(item['cantidad'])
                nueva_cantidad = max(cantidad_actual - cantidad_comprada, 0)
                stock_obj.cantidad = nueva_cantidad
                stock_obj.save()
        except Producto.DoesNotExist:
            continue
    # Vacía el carrito después del pago
    request.session['carrito'] = []
    request.session.modified = True
    return render(request, 'pago_exito.html')

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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Usuario.objects.get(correo=email)
            # Verifica tanto para hash como para texto plano (por si tienes usuarios antiguos)
            if check_password(password, user.contrasenna) or password == user.contrasenna:
                # Guardas el usuario en la sesión
                request.session['usuario_id'] = user.id_usuario
                request.session['usuario_nombre'] = user.nombre
                request.session['usuario_rol'] = user.rol
                return redirect('index')
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')

        return redirect('login')

    return render(request, 'login.html')

import re

def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "")
    if len(rut) < 8:
        return False
    cuerpo = rut[:-1]
    dv = rut[-1].upper()
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1
    dv_esperado = 11 - (suma % 11)
    if dv_esperado == 11:
        dv_esperado = '0'
    elif dv_esperado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_esperado)
    return dv == dv_esperado


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



#-------------CARRITO--------------#
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Producto
@require_POST


@require_POST
def agregar_al_carrito(request, id_producto):
    if request.method == 'POST':
        carrito = request.session.get('carrito', [])
        encontrado = False
        for item in carrito:
            if item['id'] == id_producto:
                item['cantidad'] += 1
                encontrado = True
                break
        if not encontrado:
            # Busca el producto en la base de datos y agrega con cantidad 1
            producto = Producto.objects.get(id_producto=id_producto)
            carrito.append({
                'id': producto.id_producto,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': 1,
                'imagen': producto.imagen,
                'subtotal': producto.precio,
                'stock': producto.stock_set.first().cantidad,
            })
        request.session['carrito'] = carrito
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def obtener_carrito(request):
    carrito = request.session.get('carrito', [])
    
    # Asegúrate de que cada ítem tenga un subtotal
    for item in carrito:
        if 'subtotal' not in item:
            item['subtotal'] = float(item['precio']) * item['cantidad']

    return JsonResponse({'carrito': carrito})

def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    envio_costo = 0
    if request.GET.get('envio') == '1':
        envio_costo = 3000

    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
    cantidad_total = sum(item['cantidad'] for item in carrito)
    descuento = 0
    if cantidad_total >= 4:
        descuento = subtotal * 0.10  # 10% de descuento

    total = subtotal + envio_costo - descuento

    context = {
        'carrito': carrito,
        'envio_costo': envio_costo,
        'descuento': descuento,
        'total': total,
    }
    return render(request, 'carrito.html', context)


@require_POST
def quitar_del_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])
    carrito = [item for item in carrito if int(item['id']) != int(id_producto)]
    request.session['carrito'] = carrito
    request.session.modified = True
    return JsonResponse({'success': True})

@require_POST
def aumentar_cantidad_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        if int(item['id']) == int(id_producto):
            item['cantidad'] += 1
            item['subtotal'] = float(item['precio']) * item['cantidad']
            break
    request.session['carrito'] = carrito
    request.session.modified = True
    return JsonResponse({'success': True})

@require_POST
def disminuir_cantidad_carrito(request, id_producto):
    carrito = request.session.get('carrito', [])
    for item in carrito:
        if int(item['id']) == int(id_producto):
            if item['cantidad'] > 1:
                item['cantidad'] -= 1
                item['subtotal'] = float(item['precio']) * item['cantidad']
            break
    request.session['carrito'] = carrito
    request.session.modified = True
    return JsonResponse({'success': True})





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

@csrf_exempt
def actualizar_stock(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cantidad = int(data.get("cantidad", 0))
            alerta = AlertaStock.objects.get(id=id)
            # Actualiza el stock real
            stock = alerta.producto.stock_set.first()
            if stock:
                stock.cantidad += cantidad
                stock.save()
                alerta.stock_actual = stock.cantidad
                alerta.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "No hay stock asociado."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})

def perfil(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    if request.method == 'POST':
        if 'cerrar' in request.POST:
            request.session.flush()
            messages.success(request, "Sesión cerrada correctamente.")
            return redirect('login')
        else:
            return redirect('index')
    return render(request, 'perfil.html')

def admin_index(request):
    productos = Producto.objects.all()
    return render(request, "admin.html", {"productos": productos})

def descontar_stock_y_limpiar_carrito(request):
    carrito = request.session.get('carrito', {})
    for producto_id, item in carrito.items():
        try:
            producto = Producto.objects.get(pk=producto_id)
            producto.stock -= item['cantidad']
            producto.save()
        except Producto.DoesNotExist:
            pass  # O maneja el error como prefieras
    request.session['carrito'] = {}
    request.session.modified = True

@csrf_exempt
def usuarios_api(request):
    if request.method == "GET":
        usuarios = list(Usuario.objects.all().values(
            "id_usuario", "nombre", "apellido", "correo", "telefono", "rol", "direccion"
        ))
        return JsonResponse(usuarios, safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            if Usuario.objects.filter(id_usuario=data["id_usuario"]).exists():
                return JsonResponse({"detail": "RUT ya registrado"}, status=400)
            if Usuario.objects.filter(correo=data["correo"]).exists():
                return JsonResponse({"detail": "Correo ya registrado"}, status=400)
            usuario = Usuario(
                id_usuario=data["id_usuario"],
                nombre=data["nombre"],
                apellido=data["apellido"],
                correo=data["correo"],
                contrasenna=data["contrasenna"],
                direccion=data.get("direccion", ""),
                telefono=str(data.get("telefono", "")),
                rol=data.get("rol", "cliente"),
            )
            usuario.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    else:
        return JsonResponse({"detail": "Método no permitido"}, status=405)
@csrf_exempt
def usuario_detalle_api(request, id_usuario):
    try:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
    except Usuario.DoesNotExist:
        return JsonResponse({"detail": "Usuario no encontrado"}, status=404)

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            usuario.nombre = data.get("nombre", usuario.nombre)
            usuario.apellido = data.get("apellido", usuario.apellido)
            usuario.correo = data.get("correo", usuario.correo)
            usuario.direccion = data.get("direccion", usuario.direccion)
            usuario.telefono = str(data.get("telefono", usuario.telefono))
            usuario.rol = data.get("rol", usuario.rol)
            if data.get("contrasenna"):
                usuario.contrasenna = data["contrasenna"]
            usuario.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    elif request.method == "DELETE":
        usuario.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"detail": "Método no permitido"}, status=405)