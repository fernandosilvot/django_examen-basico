from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Categoria, SubCategoria, Producto, Carrito, DetalleCarrito, RegistroEnvio
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required
from django.contrib import messages

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


@login_required
def sobre_fundacion(request):
    perfil = request.session.get('perfil')
    
    context = {
        'perfil': perfil
    }
    
    return render(request, 'store/about.html', context)


@login_required
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')
    
    context = {
        'producto': producto,
        'perfil': perfil
    }
    
    return render(request, 'store/product.html', context)


@login_required
@role_required('admin', 'cliente')
def agregar_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    perfil = request.session.get('perfil')
    
    carrito = Carrito.objects.create(usuario=request.user)
    
    carrito.detalles.create(producto=producto, cantidad=1, precio_unitario=producto.precio)
    
    return redirect('inicio')


@login_required
@role_required('admin', 'cliente')
def ver_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user, activo=True)
    perfil = request.session.get('perfil')
    
    context = {
        'carrito': carrito,
        'perfil': perfil
    }
    
    return render(request, 'store/cart.html', context)


@login_required
@role_required('admin', 'cliente')
def eliminar_producto_carrito(request, id):
    detalle = get_object_or_404(DetalleCarrito, id=id)
    detalle.delete()
    
    return redirect('ver_carrito')


@login_required
def registro_envio(request):
    carrito = Carrito.objects.get(usuario=request.user, activo=False)
    perfil = request.session.get('perfil')
    
    context = {
        'carrito': carrito,
        'perfil': perfil
    }
    
    return render(request, 'store/checkout.html', context)


@login_required
@role_required('admin', 'cliente')
def confirmar_envio(request, id):
    carrito = get_object_or_404(Carrito, id=id)
    direccion = request.POST.get('direccion')
    ciudad = request.POST.get('ciudad')
    region = request.POST.get('region')
    pais = request.POST.get('pais')
    codigo_postal = request.POST.get('codigo_postal')

    registro_envio = RegistroEnvio.objects.create(
        carrito=carrito,
        direccion=direccion,
        ciudad=ciudad,
        region=region,
        pais=pais,
        codigo_postal=codigo_postal
    )

    carrito.activo = False
    carrito.save()

    return redirect('inicio')


@login_required
@role_required('admin', 'cliente')
def ver_envios(request):
    envios = RegistroEnvio.objects.filter(carrito__usuario=request.user)
    perfil = request.session.get('perfil')

    context = {
        'envios': envios,
        'perfil': perfil
    }

    return render(request, 'store/envios.html', context)
