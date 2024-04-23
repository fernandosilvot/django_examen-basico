from django.shortcuts import render, redirect, get_object_or_404 # Se importan las funciones necesarias para renderizar y redirigir.
from django.contrib.auth.models import User # Se importa el modelo de usuario.
from django.contrib.auth.decorators import login_required # Se importa el decorador para requerir inicio de sesión.
from .models import UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio # Se importan los modelos necesarios.
from django.contrib.auth import authenticate, login, logout # Se importan las funciones necesarias para autenticar y cerrar sesión.
from .decorators import role_required # Se importa el decorador para requerir un rol específico.
from django.contrib import messages # Se importan las funciones necesarias para mostrar mensajes.
from django.db.models import Sum # Se importa la función necesaria para sumar.

def inicio_sesion(request):
    """
    Vista para el inicio de sesión de usuarios.
    """
    # aqui se verifica si el usuario esta en la base de datos y si la contraseña es correcta
    if request.method == 'POST':
        usuario = request.POST.get('usuario') # Se obtiene el nombre de usuario del formulario.
        password = request.POST.get('password') # Se obtiene la contraseña del formulario.
        
        user = authenticate(request, username=usuario, password=password) # Se autentica al usuario.
        
        if user is not None: # Si el usuario existe y la contraseña es correcta.
            profile = UserProfile.objects.get(user=user) # Se obtiene el perfil del usuario.
            
            request.session['perfil'] = profile.role # Se guarda el rol del usuario en la sesión.
            
            login(request, user) # Se inicia sesión.
            return redirect('inicio') # Se redirige al usuario a la página de inicio.
        else: # Si el usuario no existe o la contraseña es incorrecta.
            contexto = {
                'error': 'Usuario o contraseña incorrectos, intente nuevamente' # Se muestra un mensaje de error.
            }
            return render(request, 'auth/inicio_sesion.html', contexto) # Se renderiza la página de inicio de sesión.
        
    return render(request, 'auth/inicio_sesion.html') # Se renderiza la página de inicio de sesión.

def registro_usuario(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        email = request.POST.get('email') # Se obtiene el correo electrónico del formulario.
        role = "cliente" # Se define el rol del usuario como cliente.
        
        if User.objects.filter(username=usuario).exists(): # Si el nombre de usuario ya está en uso.
            messages.error(request, 'El nombre de usuario ya está en uso.') # Se muestra un mensaje de error.
            return render(request, 'auth/registro.html') # Se renderiza la página de registro.
        
        if User.objects.filter(email=email).exists(): # Si el correo electrónico ya está en uso.
            messages.error(request, 'El correo electrónico ya está en uso.') # Se muestra un mensaje de error.
            return render(request, 'auth/registro.html') # Se renderiza la página de registro.
        
        user = User.objects.create_user(username=usuario, password=password, email=email) # Se crea el usuario.
        
        UserProfile.objects.create(user=user, role=role, activo_subscripcion=False, precio_subscripcion=0) # Se crea el perfil del usuario con el rol de cliente, sin suscripción y precio de suscripción en 0.
        
        return redirect('inicio_sesion') # Se redirige al usuario a la página de inicio de sesión.
    
    return render(request, 'auth/registro.html')


@login_required
@role_required('admin', 'cliente')
def logout_view(request):
    """
    Vista para cerrar sesión de usuarios.
    """
    logout(request) # Se cierra la sesión del usuario.
    return redirect('inicio') # Se redirige al usuario a la página de inicio.


def inicio(request):
    """
    Vista para la página de inicio.
    """
    categorias = Categoria.objects.all() # Se obtienen todas las categorías.
    subcategoria = SubCategoria.objects.all() # Se obtienen todas las subcategorías.
    productos = Producto.objects.all() # Se obtienen todos los productos.
    carrito = Carrito.objects.all() # Se obtienen todos los carritos.
    perfil = request.session.get('perfil') # Se obtiene el perfil del usuario.
    
    context = {
        'categorias': categorias, # Se envían las categorías al contexto.
        'subcategoria': subcategoria, # Se envían las subcategorías al contexto.
        'productos': productos, # Se envían los productos al contexto.
        'carrito': carrito, # Se envían los carritos al contexto.
        'perfil': perfil # Se envía el perfil al contexto.
    }
    
    return render(request,'store/index.html', context) # Se renderiza la página de inicio con el contexto.


def sobre_fundacion(request):
    """
    Vista para la página 'Sobre la fundación'.
    """
    perfil = request.session.get('perfil') # Se obtiene el perfil del usuario.
    categorias = Categoria.objects.all() # Se obtienen todas las categorías.
    
    context = {
        'perfil': perfil, # Se envía el perfil al contexto.
        'categorias': categorias, # Se envían las categorías al contexto.
    }
    
    return render(request, 'store/about.html', context) # Se renderiza la página 'Sobre la fundación' con el contexto.

@login_required # Se requiere que el usuario esté autenticado.
@role_required('admin', 'cliente') # Se requiere que el usuario tenga el rol de administrador o cliente.
def Compra_subscripcion(request):
    """
    Vista para la compra de suscripciones.
    """
    profile = request.session.get('perfil') # Se obtiene el perfil del usuario.
    perfil = UserProfile.objects.get(user=request.user) # Se obtiene el perfil del usuario.
    categorias = Categoria.objects.all() # Se obtienen todas las categorías.
    
    if request.method == 'POST':
        accion = request.POST.get('accion') # Se obtiene la acción del formulario.
        
        if accion == 'subscribirse': # Si la acción es subscribirse.
            precio_subscripcion = request.POST.get('precio') # Se obtiene el precio de la suscripción.
            if precio_subscripcion is not None: # Si el precio de la suscripción no es nulo.
                perfil.activo_subscripcion = True # Se activa la suscripción del usuario.
                perfil.precio_subscripcion = precio_subscripcion # Se guarda el precio de la suscripción.
                perfil.save() # Se guarda el perfil del usuario.
                messages.success(request, '¡Te has suscrito correctamente!') # Se muestra un mensaje de éxito.
                return redirect('inicio') # Se redirige al usuario a la página de inicio.
            else: # Si el precio de la suscripción es nulo.
                messages.error(request, 'Por favor, ingresa el precio de la suscripción.') # Se muestra un mensaje de error.
                return redirect('compra_subscripcion') # Se redirige al usuario a la página de compra de suscripción.
        
        elif accion == 'cancelar': # Si la acción es cancelar.
            perfil.activo_subscripcion = False # Se desactiva la suscripción del usuario.
            perfil.precio_subscripcion = 0 # Se establece el precio de la suscripción en 0.
            perfil.save() # Se guarda el perfil del usuario.
            messages.success(request, '¡Has cancelado tu suscripción correctamente!') # Se muestra un mensaje de éxito.
            return redirect('inicio') # Se redirige al usuario a la página de inicio.
    
    context = {
        'perfil': perfil, # Se envía el perfil al contexto.
        'profile':profile, 
        'categorias': categorias, # Se envían las categorías al contexto.
    }
    
    return render(request, 'store/subscripcion.html', context) # Se renderiza la página de compra de suscripción con el contexto.


def detalle_producto(request, id):
    """
    Vista para ver los detalles de un producto.
    """
    producto = get_object_or_404(Producto, id=id) # Se obtiene el producto por su ID.
    perfil = request.session.get('perfil') # Se obtiene el perfil del usuario.
    categorias = Categoria.objects.all() # Se obtienen todas las categorías.
    
    context = {
        'producto': producto, # Se envía el producto al contexto.
        'perfil': perfil, # Se envía el perfil al contexto.
        'categorias': categorias, # Se envían las categorías al contexto.
    }
    
    return render(request, 'store/product.html', context) # Se renderiza la página de detalles del producto con el contexto.


@login_required
@role_required('admin', 'cliente')
def agregar_carrito(request, id): 
    """
    Vista para agregar un producto al carrito.
    """
    producto = get_object_or_404(Producto, id=id) # Se obtiene el producto por su ID.
    perfil = request.session.get('perfil')
    
    
    carritos_activos = Carrito.objects.filter(usuario=request.user, activo=True) # Se obtienen los carritos activos del usuario
    
    if carritos_activos.exists(): # Si hay carritos activos
        carrito = carritos_activos.first() # Se selecciona el primer carrito activo
    else:
        carrito = Carrito.objects.create(usuario=request.user)# Si no hay carritos activos, crea uno nuevo
    
    detalle_carrito = DetalleCarrito.objects.create(# Crea un nuevo detalle de carrito para agregar el producto
        carrito=carrito, # Asigna el carrito al detalle
        precio_unitario=producto.precio_normal # Asigna el precio unitario del producto al detalle
    )
    
    detalle_carrito.productos.add(producto) # Agrega el producto al detalle
    
    return redirect('inicio') # Redirige al usuario a la página de inicio


@login_required
@role_required('admin', 'cliente')
def ver_carrito(request):
    """
    Vista para ver el carrito de compras.
    """
    try:
        carrito = Carrito.objects.get(usuario=request.user, activo=True)
        
        # Calculamos el subtotal para cada detalle en el carrito
        for detalle in carrito.detalles.all():
            detalle.subtotal = detalle.productos.first().precio_final() * detalle.cantidad # Se calcula el subtotal del detalle
            detalle.save() # Se guarda el detalle
            
        # Calculamos el total de la venta
        total_venta = carrito.detalles.all().aggregate(Sum('subtotal'))['subtotal__sum']
    except Carrito.DoesNotExist:
        carrito = None # Si no hay carrito activo, se establece como nulo
        total_venta = 0 # Si no hay carrito activo, el total de la venta es 0
    
    perfil = request.session.get('perfil') 
    
    context = {
        'carrito': carrito,
        'perfil': perfil,
        'total_venta': total_venta,
    }
    
    return render(request, 'store/cart.html', context)


@login_required
@role_required('admin', 'cliente')
def eliminar_producto_carrito(request, id):
    """
    Vista para eliminar un producto del carrito.
    """
    detalle = get_object_or_404(DetalleCarrito, id=id) # Se obtiene el detalle del carrito por su ID
    detalle.delete() # Se elimina el detalle del carrito
    
    return redirect('ver_carrito') # Se redirige al usuario a la página del carrito


@login_required
@role_required('admin', 'cliente')
def checkout(request):
    """
    Vista para realizar el checkout de la compra.
    """
    # Obtener el carrito activo del usuario
    carrito = Carrito.objects.get(usuario=request.user, activo=True)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()
    
    # Obtener los detalles del carrito
    detalles_carrito = carrito.detalles.all()
    
    # Calcular el total de la compra
    total = sum(detalle.subtotal for detalle in detalles_carrito)
    
    if request.method == 'POST':
        # Procesar el formulario enviado por el usuario
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        region = request.POST.get('region')
        pais = request.POST.get('pais')
        codigo_postal = request.POST.get('codigo_postal')
        
        # Crear un registro de envío
        registro_envio = RegistroEnvio.objects.create(
            carrito=carrito,
            detalle=detalles_carrito.first(),  # Aquí seleccionamos el primer detalle del carrito
            direccion=direccion, # Asignamos la dirección
            ciudad=ciudad, # Asignamos la ciudad
            region=region, # Asignamos la región
            pais=pais, # Asignamos el país
            codigo_postal=codigo_postal # Asignamos el código postal
        )
        
        carrito.activo = False # Se desactiva el carrito
        carrito.save() # Se guarda el carrito
        
        # Descontar los productos vendidos del stock
        for detalle in detalles_carrito:
            for producto in detalle.productos.all():
                producto.stock -= detalle.cantidad
                producto.save()
        
        # Redirigir al usuario a una página de confirmación
        return redirect('confirmacion_envio', id=carrito.id)
    
    context = {
        'carrito': carrito,
        'detalles_carrito': detalles_carrito,
        'total': total,
        'perfil': perfil,
        'categorias': categorias,
    }
    
    return render(request, 'store/checkout.html', context)

@login_required
@role_required('admin', 'cliente')
def confirmacion_envio(request, id):
    """
    Vista para la confirmación de envío.

    """
    # Obtener el carrito y el registro de envío
    carrito = get_object_or_404(Carrito, id=id)
    registro_envio = RegistroEnvio.objects.get(carrito=carrito)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()

    # Verificar que el carrito pertenezca al usuario logueado
    if carrito.usuario != request.user:
        # Si no pertenece, redirigir a una página de error o a donde sea necesario
        return redirect('inicio')  # Por ejemplo, redirigir al inicio

    # Calculamos el total de la compra
    total_venta = carrito.detalles.aggregate(total=Sum('subtotal'))['total'] or 0

    context = {
        'carrito': carrito,
        'registro_envio': registro_envio,
        'total_venta': total_venta,
        'perfil': perfil,
        'categorias': categorias,
    }

    return render(request, 'store/confirmacion_envio.html', context)

@login_required
@role_required('admin', 'cliente')
def ver_envios(request):
    """
    Vista para ver los envíos realizados por el usuario.    
    """
    envios = RegistroEnvio.objects.filter(carrito__usuario=request.user) # Se obtienen los envíos del usuario
    perfil = request.session.get('perfil') # Se obtiene el perfil del usuario
    categorias = Categoria.objects.all() # Se obtienen todas las categorías

    context = {
        'envios': envios,
        'perfil': perfil,
        'categorias': categorias,
    }

    return render(request, 'store/envios.html', context)

def buscar_producto(request):
    """
    Vista para buscar productos.
    """
    query = request.GET.get('q', '')  # Obtener el término de búsqueda de la URL
    categoria_id = request.GET.get('categoria')
    perfil = request.session.get('perfil')

    if categoria_id:
        # Si se selecciona una categoría, filtrar por nombre y categoría
        productos = Producto.objects.filter(
            nombre__icontains=query,
            categoria_id=categoria_id
        )
    else:
        # Si no se selecciona ninguna categoría, filtrar solo por nombre
        productos = Producto.objects.filter(nombre__icontains=query)

    context = {
        'query': query,
        'productos': productos,
        'perfil': perfil,
    }

    return render(request, 'store/busqueda.html', context)