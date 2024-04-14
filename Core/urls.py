from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.inicio, name='inicio'),
    path('fundacion/', views.sobre_fundacion, name='sobre_fundacion'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),  
    path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar-producto-carrito/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('registro-envio/', views.registro_envio, name='registro_envio'),
    path('confirmar-envio/<int:id>/', views.confirmar_envio, name='confirmar_envio'),
    path('ver-envios/', views.ver_envios, name='ver_envios'),
]
