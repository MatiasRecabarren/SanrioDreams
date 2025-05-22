from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('loading/', views.loading, name='loading'),
    path('productos/', views.productos, name='productos'),
    path('peluches/', views.peluches, name='peluches'),
    path('botellas/', views.botellas, name='botellas'),
    path('lamparas/', views.lamparas, name='lamparas'),
    path('llaveros/', views.llaveros, name='llaveros'),
    path('login/', views.login, name='login'),
    path('pines/', views.pines, name='pines'),
    path('registro/', views.registro, name='registro'),
    path('termos/', views.termos, name='termos'),
]
