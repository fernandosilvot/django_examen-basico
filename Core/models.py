from django.db import models
from django.contrib.auth import get_user_model # Se importa el modelo de usuario para la relación uno a uno.
from django.conf import settings # Se importan las configuraciones de la aplicación.

class UserProfile(models.Model):
    """
    Modelo para el perfil de usuario.

    user: Usuario asociado a este perfil.
    role: Rol del usuario.
    activo_subscripcion: Estado de la suscripción del usuario.
    precio_subscripcion: Precio de la suscripción del usuario.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.ROLES)
    activo_subscripcion = models.BooleanField(default=False)
    precio_subscripcion = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'

class Categoria(models.Model):
    """
    Modelo para las categorías de productos.

    nombre: Nombre de la categoría.
    """
    nombre = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.nombre
    
class SubCategoria(models.Model):
    """
    Modelo para las subcategorías de productos.

    tipo: Tipo de subcategoría.
    """
    animal = ( # Se define el tipo de subcategoría.
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    )
    tipo = models.CharField(max_length=20, choices=animal, default='otro')
    
    def __str__(self) -> str:
        return self.tipo
    
class Producto(models.Model):
    """
    Modelo para los productos.

    nombre: Nombre del producto.
    imagen: Imagen del producto.
    descripcion: Descripción del producto.
    animal: Subcategoría del producto.
    precio_normal: Precio normal del producto.
    promocion: Estado de promoción del producto.
    descuento: Descuento del producto.
    stock: Stock del producto.
    categoria: Categoría del producto.
    """
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
        """
        Calcula el precio final del producto, considerando cualquier descuento de promoción.
        """
        if self.promocion is True:
            return self.precio_normal - (self.precio_normal * self.descuento / 100)
        else:
            return self.precio_normal
        
    def __str__(self) -> str:
        return self.nombre

class Carrito(models.Model):
    """
    Modelo para el carrito de compras.

    usuario: Usuario que posee el carrito.
    creado_en: Fecha y hora de creación del carrito.
    actualizado_en: Fecha y hora de última actualización del carrito.
    activo: Estado de activación del carrito.
    """
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Carrito de {self.usuario.username}'

class DetalleCarrito(models.Model):
    """
    Modelo para los detalles del carrito de compras.

    carrito: Carrito al que pertenecen los detalles.
    productos: Productos incluidos en los detalles.
    cantidad: Cantidad de productos.
    precio_unitario: Precio unitario de los productos.
    subtotal: Subtotal del detalle.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    productos = models.ManyToManyField(Producto) 
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Detalle de {self.carrito.usuario.username}'

class RegistroEnvio(models.Model):
    """
    Modelo para el registro de envíos.

    carrito: Carrito asociado al envío.
    detalle: Detalle del carrito asociado al envío.
    direccion: Dirección de envío.
    ciudad: Ciudad de envío.
    region: Región de envío.
    pais: País de envío.
    codigo_postal: Código postal de envío.
    fecha_envio: Fecha y hora de envío.
    estado: Estado del envío.
    """
    estados = (
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    )
    
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='envios')
    detalle = models.ForeignKey(DetalleCarrito, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    pais = models.CharField(max_length=200)
    codigo_postal = models.CharField(max_length=200)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=estados, default='pendiente')

    def __str__(self) -> str:
        return f'Envío de {self.carrito.usuario.username}'
