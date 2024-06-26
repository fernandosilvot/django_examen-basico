"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # importamos include para incluir las urls de la app Core
from django.conf import settings # importamos settings 
from django.conf.urls.static import static # importamos static 

urlpatterns = [
    path("admin/", admin.site.urls,),
    path("", include("Core.urls")),  # incluimos las urls de la app Core
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # agregamos la configuración para servir archivos multimedia
