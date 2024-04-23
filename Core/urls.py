from django.urls import path
from . import views

urlpatterns = [
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'), # Se define la URL para la vista de inicio de sesión.
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'), # Se define la URL para la vista de registro de usuario.
    path('logout/', views.logout_view, name='logout'), # Se define la URL para la vista de cierre de sesión.
    path('', views.inicio, name='inicio'), # Se define la URL para la vista de inicio.
    path('<int:categoria_id>/', views.inicio, name='inicio_categoria'), # Se define la URL para la vista de inicio con categoría.
    path('fundacion/', views.sobre_fundacion, name='sobre_fundacion'), # Se define la URL para la vista de sobre la fundación.
    path('buscar/', views.buscar_producto, name='buscar_producto'), # Se define la URL para la vista de búsqueda de productos.
    path('compra-subscripcion/', views.Compra_subscripcion, name='Compra_subscripcion'), # Se define la URL para la vista de compra de subscripción.
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'), # Se define la URL para la vista de detalle de producto.
    path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'), # Se define la URL para la vista de agregar al carrito.
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'), # Se define la URL para la vista de ver carrito.
    path('eliminar-producto-carrito/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'), # Se define la URL para la vista de eliminar producto del carrito.
    path('checkout/', views.checkout, name='checkout'), # Se define la URL para la vista de checkout.
    path('confirmacion-envio/<int:id>/', views.confirmacion_envio, name='confirmacion_envio'), # Se define la URL para la vista de confirmación de envío.
    path('ver-envios/', views.ver_envios, name='ver_envios'), # Se define la URL para la vista de ver envíos.
]
