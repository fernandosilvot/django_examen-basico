from django.contrib import admin
from .models import  UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(RegistroEnvio)

