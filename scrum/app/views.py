from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UserModelForm



# Create your views here.

def login_usuario(request):
    if request.method=='POST':
        usuario=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usuario,password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error (request, "Usuario o contraseña incorrecta")
            return redirect('login')
    return render(request,"Login.html",{})


def inicio (request): 
    saludo = "Bienvenido %s" %(request.user)
    nombre = "Proyecto Scrum"
    context ={
        "nombre": nombre,
        "saludo": saludo,
    }
    return render(request,"inicio.html",context)


def cerrar (request):
    logout(request)
    return redirect('login')


def crear_proyecto2(request):
   
   form=ProyectoModelForm(request.POST or None)
   
   if form.is_valid():
        print("valido")
        instancia=form.save(commit=False)
        instancia.backlog_id='12345'
        instancia=form.save()
   else:
        form=ProyectoModelForm(request.POST or None)
    
    
   context={'form':form}
   
   return render(request, 'crear_proyecto2.html', context)
   
def agregar_usuario(request):
    form_usuario=UsuarioProyectoFormulario(request or None)

    if form_usuario.is_valid():
       print("valido")
       instancia2=form_usuario.save(commit=False)
       instancia.backlog_id='12345'
       instancia=form_usuario.save()

    else:
       form_usuario=UsuarioProyectoFormulario(request or None)

    context={'form_usuario':form_usuario}

    return render(request, 'crear_proyecto2.html', context)


def crear_usuario(request):
    form= UserModelForm(request.POST or None)
    if form.is_valid():
        instance= form.save(commit=False)
        instance.date_joined=timezone.now()
        instance.is_active=True
        instance.is_staff=False
        instance.is_superuser= False
        if User.objects.filter(email=instance.email).exists():
            messages.error (request, f'''email
                                         El email ya esta registrado''')
        else:
            messages.success(request,"Usuario creado con exito, ya puedes iniciar sesión")
            instance= form.save()
            return redirect('login')    
    else:
        form= UserModelForm(request.POST or None)       
    context ={
        "form": form,
    }
    return render(request,"crear_usuarios.html",context)


def ver_perfil(request):
    saludo = "Bienvenido %s" %(request.user)
    nombre = "Proyecto Scrum"
    context ={
        "nombre": nombre,
        "saludo": saludo,
    }
    return render(request,'ver_perfil.html',context)

def editar_perfil(request):
    context ={
    }
    return render(request,'modificar_usuario.html',context)

def listar_proyectos(request):

    proyectos = Proyecto.objects.all()
    context = {'proyectos': proyectos}

    return render(request, "listar_proyectos.html",context)

'''
#####
#ELIMINACION DIRECTA
#####

 #eliminacion directa sin el metodo POST
def eliminar(request, backlog_id):

    proyecto = Proyecto.objects.get(backlog_id = backlog_id)
    #se elimina de la base de datos
    proyecto.delete()
    return redirect('ver_proyectos')

#eliminacion directo con el Metodo POST
def eliminar(request, backlog_id):

    proyecto = Proyecto.objects.get(backlog_id = backlog_id)
    
    if request.method == 'POST':
        proyecto.delete()
        return redirect('ver_proyectos')
    
    context = {'proyecto': proyecto}
    return render(request, 'eliminar.html',context)

#####
#ELIMINACION lOGICA
#cambiar el estado de una instancia en concreto
#es decir, si tenemos un atributo estado, entonces podriamos
#cambiar el estado de dicho objeto. ejemplo podriamos haber definido
#el estado de cada proyecto con TRUE y luego cambiar de estado a FALSE
#####
'''

