from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib import messages
from django.db.models import Sum
from .forms import LoginForm, RegisterForm

def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usuario')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                profile = UserProfile.objects.get(user=user)
                request.session['perfil'] = profile.role
                login(request, user)
                return redirect('inicio')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos, intente nuevamente')
    else:
        form = LoginForm()
    return render(request, 'auth/inicio_sesion.html', {'form': form})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            UserProfile.objects.create(user=user, role="cliente", activo_subscripcion=False, precio_subscripcion=0)
            return redirect('inicio_sesion')
    else:
        form = RegisterForm()
    return render(request, 'auth/registro.html', {'form': form})

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
    
    carritos_activos = Carrito.objects.filter(usuario=request.user, activo=True)
    
    if carritos_activos.exists():
        carrito = carritos_activos.first()
    else:
        carrito = Carrito.objects.create(usuario=request.user)
    
    detalle_carrito = DetalleCarrito.objects.create(
        carrito=carrito,
        precio_unitario=producto.precio_normal
    )
    
    detalle_carrito.productos.add(producto)
    
    return redirect('inicio')

@login_required
@role_required('admin', 'cliente')
def ver_carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user, activo=True)
        
        for detalle in carrito.detalles.all():
            detalle.subtotal = detalle.productos.first().precio_final() * detalle.cantidad
            detalle.save()
            
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
    carrito = Carrito.objects.get(usuario=request.user, activo=True)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()
    detalles_carrito = carrito.detalles.all()
    total = sum(detalle.subtotal for detalle in detalles_carrito)
    
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        region = request.POST.get('region')
        pais = request.POST.get('pais')
        codigo_postal = request.POST.get('codigo_postal')
        
        registro_envio = RegistroEnvio.objects.create(
            carrito=carrito,
            detalle=detalles_carrito.first(),
            direccion=direccion,
            ciudad=ciudad,
            region=region,
            pais=pais,
            codigo_postal=codigo_postal
        )
        
        carrito.activo = False
        carrito.save()
        
        for detalle in detalles_carrito:
            for producto in detalle.productos.all():
                producto.stock -= detalle.cantidad
                producto.save()
        
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
    carrito = get_object_or_404(Carrito, id=id)
    registro_envio = RegistroEnvio.objects.get(carrito=carrito)
    perfil = request.session.get('perfil')
    categorias = Categoria.objects.all()

    if carrito.usuario != request.user:
        return redirect('inicio')

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
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria')
    perfil = request.session.get('perfil')

    if categoria_id:
        productos = Producto.objects.filter(
            nombre__icontains=query,
            categoria_id=categoria_id
        )
    else:
        productos = Producto.objects.filter(nombre__icontains=query)

    context = {
        'query': query,
        'productos': productos,
        'perfil': perfil,
    }

    return render(request, 'store/busqueda.html', context)