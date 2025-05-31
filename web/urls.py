from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('loading/', views.loading, name='loading'),
    path('productos/', views.productos, name='productos'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-al-carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('aumentar-cantidad/<int:id_producto>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir-cantidad/<int:id_producto>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('eliminar-producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('obtener-cantidad-carrito/', views.obtener_cantidad_carrito, name='obtener_cantidad_carrito'),



 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)