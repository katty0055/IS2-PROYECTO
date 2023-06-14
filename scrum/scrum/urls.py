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
    path('ver_perfil/',views.ver_perfil,name='ver_perfil'),
    path('modificar_usuario',views.editar_perfil,name='modificar_usuario'),
    path('modificar_password',views.editar_password,name='modificar_password'),
    path('eliminar_usuario',views.eliminar_usuario,name='eliminar_usuario'),
    path('crear_proyecto/',views.crear_proyecto,name='crear_proyecto'),
    path('agregar_usuario_proyecto/<str:pk>/',views.agregar_usuario_proyecto,name='agregar_usuario_proyecto'),
    path('listar_proyectos/modificar_proyecto/<str:pk>/',views.modificar_proyecto,name='modificar_proyecto'),
    path('listar_proyectos/', views.listar_proyectos, name='listar_proyectos'),
    path('listar_proyectos/eliminar_proyecto/<str:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('listar_proyectos/crear_sprint_proyecto/<str:pk>/', views.crear_sprint_proyecto, name='crear_sprint_proyecto'),
    path('listar_proyectos/listar_sprint_proyecto/', views.listar_sprint_proyecto, name='listar_sprint_proyecto'),
    path('listar_proyectos/listar_sprint_proyecto/modificar_sprint_proyecto/<str:pk>/', views.modificar_sprint_proyecto, name='modificar_sprint_proyecto'),
    path('listar_proyectos/user_story/<str:pk>/', views.crear_user_story, name='crear_user_story'),
    path('listar_proyectos/listar_us/', views.listar_us, name='listar_us'),
    path('modificar_user_story/<int:pk>/', views.editar_user_story, name='modificar_user_story'),
    path('listar_proyectos/backlog/<str:pk>', views.backlog, name='backlog'),
    path('listar_proyectos/backlog/modificar_sprint_proyecto/<str:pk>/', views.modificar_sprint_proyecto, name='modificar_sprint_proyecto'),
    path('listar_proyectos/backlog/modificar_sprint_proyecto/<str:pk>/backlog/', views.modificar_sprint_proyecto, name='modificar_sprint_proyecto'),
    path('listar_proyectos/backlog/eliminar_sprint/<str:pk>/', views.eliminar_sprint, name='eliminar_sprint'),
    path('listar_proyectos/backlog/cancelar_us/<str:pk>/', views.eliminar_user_story, name='cancelar_us'),
    path('listar_proyectos/backlog/seleccionar_us/<str:pk>/', views.asignar_us_a_sprint, name='seleccionar_us'),
    path('listar_proyectos/backlog/iniciar_sprint/<str:pk>/<str:accion>/', views.iniciar_cerrar_sprint),
    path('listar_proyectos/kanban/<str:pk>/', views.ver_kanban, name='kanban'),
    path('listar_proyectos/burndown_chart/<str:pk>/', views.burndown_chart, name='burndown_chart'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


