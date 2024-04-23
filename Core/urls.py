from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.inicio, name='inicio'),
    path('<int:categoria_id>/', views.inicio, name='inicio_categoria'),
    path('fundacion/', views.sobre_fundacion, name='sobre_fundacion'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('compra-subscripcion/', views.Compra_subscripcion, name='Compra_subscripcion'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),  
    path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar-producto-carrito/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion-envio/<int:id>/', views.confirmacion_envio, name='confirmacion_envio'),
    path('ver-envios/', views.ver_envios, name='ver_envios'),
]
