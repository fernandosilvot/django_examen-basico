from django.contrib import admin
from .models import  UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio # Importamos los modelos de la aplicación Core.

# Registrando los modelos en el panel de administración de Django

admin.site.register(UserProfile) # Se registra el modelo UserProfile.
admin.site.register(Categoria) # Se registra el modelo Categoria.
admin.site.register(SubCategoria) # Se registra el modelo SubCategoria.
admin.site.register(Producto) # Se registra el modelo Producto.
admin.site.register(Carrito)# Se registra el modelo Carrito.
admin.site.register(DetalleCarrito) # Se registra el modelo DetalleCarrito.
admin.site.register(RegistroEnvio) # Se registra el modelo RegistroEnvio.

