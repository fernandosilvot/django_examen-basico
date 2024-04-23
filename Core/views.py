from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib import messages
from django.db.models import Sum, Q

def inicio_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=password)
        
        if user is not None:
            profile = UserProfile.objects.get(user=user)
            
            request.session['perfil'] = profile.role
            
            login(request, user)
            return redirect('inicio')
        else:
            contexto = {
                'error': 'Usuario o contraseña incorrectos, intente nuevamente'
            }
            return render(request, 'auth/inicio_sesion.html', contexto)
        
    return render(request, 'auth/inicio_sesion.html')

def registro_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = "cliente"
        
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'auth/registro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está en uso.')
            return render(request, 'auth/registro.html')
        
        user = User.objects.create_user(username=usuario, password=password, email=email)
        
        UserProfile.objects.create(user=user, role=role, activo_subscripcion=False, precio_subscripcion=0)
        
        return redirect('inicio_sesion')
    
    return render(request, 'auth/registro.html')


@login_required
@role_required('admin', 'cliente')
def logout_view(request):
    logout(request)
    return redirect('inicio')


def inicio(request):
    categorias = Categoria.objects.all()
    subcategoria = SubCategoria.objects.all()
    productos = Producto.objects.all()
    carrito = Carrito.objects.all()
    perfil = request.session.get('perfil')
    
    context = {
        'categorias': categorias,
        'subcategoria': subcategoria,
        'productos': productos,
        'carrito': carrito,
        'perfil': perfil
    }
    
    return render(request,'store/index.html', context)


def sobre_fundacion(request):
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()
    
    context = {
        'perfil': perfil,
        'categorias': categorias,
    }
    
    return render(request, 'store/about.html', context)

@login_required
@role_required('admin', 'cliente')
def Compra_subscripcion(request):
    profile = request.session.get('perfil')
    perfil = UserProfile.objects.get(user=request.user)
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'subscribirse':
            precio_subscripcion = request.POST.get('precio')
            if precio_subscripcion is not None:
                perfil.activo_subscripcion = True
                perfil.precio_subscripcion = precio_subscripcion
                perfil.save()
                messages.success(request, '¡Te has suscrito correctamente!')
                return redirect('inicio')
            else:
                messages.error(request, 'Por favor, ingresa el precio de la suscripción.')
                return redirect('compra_subscripcion')
        
        elif accion == 'cancelar':
            perfil.activo_subscripcion = False
            perfil.precio_subscripcion = 0
            perfil.save()
            messages.success(request, '¡Has cancelado tu suscripción correctamente!')
            return redirect('inicio')
    
    context = {
        
        'perfil': perfil,
        'profile':profile,
        'categorias': categorias,
    }
    
    return render(request, 'store/subscripcion.html', context)


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()
    
    context = {
        'producto': producto,
        'perfil': perfil,
        'categorias': categorias,
    }
    
    return render(request, 'store/product.html', context)


@login_required
@role_required('admin', 'cliente')
def agregar_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')
    
    # Busca si ya existe un carrito activo para el usuario, sino, lo crea
    carritos_activos = Carrito.objects.filter(usuario=request.user, activo=True)
    
    if carritos_activos.exists():
        # Si hay carritos activos, usa el primero encontrado
        carrito = carritos_activos.first()
    else:
        # Si no hay carritos activos, crea uno nuevo
        carrito = Carrito.objects.create(usuario=request.user)
    
    # Crea un nuevo detalle de carrito para agregar el producto
    detalle_carrito = DetalleCarrito.objects.create(
        carrito=carrito,
        precio_unitario=producto.precio_normal
    )
    
    # Agrega el producto al detalle de carrito
    detalle_carrito.productos.add(producto)
    
    return redirect('inicio')


@login_required
@role_required('admin', 'cliente')
def ver_carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user, activo=True)
        
        # Calculamos el subtotal para cada detalle en el carrito
        for detalle in carrito.detalles.all():
            detalle.subtotal = detalle.productos.first().precio_final() * detalle.cantidad
            detalle.save()
            
        # Calculamos el total de la venta
        total_venta = carrito.detalles.all().aggregate(Sum('subtotal'))['subtotal__sum']
    except Carrito.DoesNotExist:
        carrito = None
        total_venta = 0
    
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
    detalle = get_object_or_404(DetalleCarrito, id=id)
    detalle.delete()
    
    return redirect('ver_carrito')


@login_required
@role_required('admin', 'cliente')
def checkout(request):
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
            direccion=direccion,
            ciudad=ciudad,
            region=region,
            pais=pais,
            codigo_postal=codigo_postal
        )
        
        # Marcar el carrito como inactivo
        carrito.activo = False
        carrito.save()
        
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
    envios = RegistroEnvio.objects.filter(carrito__usuario=request.user)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()

    context = {
        'envios': envios,
        'perfil': perfil,
        'categorias': categorias,
    }

    return render(request, 'store/envios.html', context)

def buscar_producto(request):
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
