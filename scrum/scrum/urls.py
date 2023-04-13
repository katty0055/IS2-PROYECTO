"""scrum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_usuario,name='login'),
    path('login',views.crear_usuario,name='crear_usuario'),
    path('inicio/',views.inicio, name='inicio'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('crear_proyecto2/',views.crear_proyecto2,name='crear_proyecto2'),
    path('agregar_usuario/',views.agregar_usuario,name='agregar_usuario'),
    path('ver_perfil/',views.ver_perfil,name='ver_perfil'),
    path('modificar_perfil/',views.editar_perfil,name='editar_perfil'),
    path('ver_proyectos/', views.ver_proyectos, name='ver_proyectos')
]    
    

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


