from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import agregar_al_carrito, obtener_carrito

urlpatterns = [
    path('', views.index, name='index'),
    path('loading/', views.loading, name='loading'),
    path('productos/', views.productos, name='productos'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('informes_stock/', views.informes_stock, name='informes_stock'),
    path('agregar-al-carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('obtener-carrito/', views.obtener_carrito, name='obtener_carrito'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('quitar-del-carrito/<int:id_producto>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('admin/', views.admin_index, name='admin_index'),
    path('carrito/aumentar/<int:id_producto>/', views.aumentar_cantidad_carrito, name='aumentar_cantidad_carrito'),
    path('carrito/disminuir/<int:id_producto>/', views.disminuir_cantidad_carrito, name='disminuir_cantidad_carrito'),
    path('carrito/quitar/<int:id_producto>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('pago/transferencia/', views.pago_transferencia, name='pago_transferencia'),
    path('pago/tarjeta/', views.pago_tarjeta, name='pago_tarjeta'),
    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('perfil/', views.perfil, name='perfil'),
    path('pago/', views.pago, name='pago'),
    path('actualizar-stock/<int:id>/', views.actualizar_stock, name='actualizar_stock'),
    path('usuarios/', views.usuarios_api, name='usuarios_api'),
    path('usuarios/<str:id_usuario>', views.usuario_detalle_api, name='usuario_detalle_api'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)