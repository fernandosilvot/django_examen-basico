from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.ROLES)
    activo_subscripcion = models.BooleanField(default=False)
    precio_subscripcion = models.IntegerField(default=0)
    
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'


    
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.nombre
    
class SubCategoria(models.Model):
    animal = (
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    )
    tipo = models.CharField(max_length=20, choices=animal, default='otro')
    
    def __str__(self) -> str:
        return self.tipo
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True, default='productos/default.jpg')
    descripcion = models.TextField(null=True, blank=True)
    animal = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name='productos')
    precio_normal = models.IntegerField(default=0)
    promocion = models.BooleanField(default=False)
    descuento = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
 
    def precio_final(self):
        if self.promocion is True:
            return self.precio_normal - (self.precio_normal * self.descuento / 100)
        else:
            return self.precio_normal
        
    def __str__(self) -> str:
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Carrito de {self.usuario.username}'

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    productos = models.ManyToManyField(Producto) 
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Detalle de {self.carrito.usuario.username}'

class RegistroEnvio(models.Model):
    estados = (
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    )
    
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='envios')
    detalle = models.ForeignKey(DetalleCarrito, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=200)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=estados, default='pendiente') 

    def __str__(self) -> str:
        return f'Envio de {self.carrito.usuario.username}'