from django.db import models
from django.contrib.auth.hashers import make_password
import re

# Opciones para el campo rol
ROL_OPCIONES = (
    ('cliente', 'Cliente'),
    ('empleado', 'Empleado'),
    ('admin', 'Administrador'),
)

class Usuario(models.Model):
    id_usuario = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasenna = models.CharField(max_length=128)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=9)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expira = models.DateTimeField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_OPCIONES, default='cliente')

    class Meta:
        managed = False  # Evita que Django gestione esta tabla
        db_table = 'USUARIO'  # Especifica el nombre de la tabla en Oracle

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"


    def __str__(self):
        return self.correo

    def save(self, *args, **kwargs):
        if not self.pk or 'contrasenna' in kwargs.get('update_fields', []):
            self.contrasenna = make_password(self.contrasenna)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"

    @staticmethod
    def validar_rut(rut):
        rut = rut.replace('.', '').lower().replace('-', '')
        if not re.match(r'^\d{7,8}[kK0-9]$', rut):
            return False
        cuerpo = rut[:-1]
        dv = rut[-1]
        suma = sum(int(d) * (2 + i % 6) for i, d in enumerate(reversed(cuerpo)))
        resto = suma % 11
        digito = 'k' if 11 - resto == 10 else str(11 - resto)
        return digito.lower() == dv.lower()

    @staticmethod
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

class TipoEmpleado(models.Model):
    id_tipo_empleado = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    id_empleado = models.CharField(max_length=12, primary_key=True)  # RUT
    fecha_contratacion = models.DateField()
    tipo = models.ForeignKey(TipoEmpleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_empleado} ({self.tipo.descripcion})"

class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.CharField(max_length=255)  # O usa ImageField si manejas archivos
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    ubicacion_detalle = models.CharField(max_length=255)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} en {self.ubicacion_detalle}"

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"Carrito #{self.id_carrito} - {self.estado}"

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pago #{self.id_pago} - {self.estado}"

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.estado}"

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    productos = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle #{self.id_detalle} - Pedido #{self.pedido.id_pedido}"

class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_envio = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} para {self.usuario.nombre}"

class Resenna(models.Model):
    id_resenna = models.AutoField(primary_key=True)
    comentario = models.TextField(blank=True, null=True)
    valoracion = models.PositiveSmallIntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reseña de {self.usuario.nombre} sobre {self.producto.nombre}"

