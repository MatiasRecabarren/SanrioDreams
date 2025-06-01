from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import agregar_al_carrito, obtener_carrito

urlpatterns = [

    
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('loading/', views.loading, name='loading'),
    path('productos/', views.productos, name='productos'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('informes_stock/', views.informes_stock, name='informes_stock'),
    path('actualizar-stock/<int:alerta_id>/', views.actualizar_stock, name='actualizar_stock'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('agregar-al-carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('obtener-carrito/', obtener_carrito, name='obtener_carrito'),
    path('admin/', views.admin_index, name='admin_index'),
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)