from functools import wraps # Importamos wraps
from django.shortcuts import redirect # Importamos redirect

# @role_required('admin', 'cliente')
def role_required(*roles): # Se define la función role_required con los roles como argumentos.
    def decorator(view_func): # Se define el decorador con la función view_func como argumento.
        @wraps(view_func) # Se envuelve la función view_func.
        def wrapper(request, *args, **kwargs): # Se define la función wrapper con los argumentos request, *args y **kwargs.
            if 'perfil' in request.session and request.session['perfil'] in roles: # Si el perfil está en la sesión y el perfil está en los roles.
                return view_func(request, *args, **kwargs) # Se retorna la función view_func con los argumentos request, *args y **kwargs.
            else: 
                return redirect('/')  # Se redirige a la URL '/'.
        return wrapper # Se retorna la función wrapper.
    return decorator # Se retorna el decorador.
    