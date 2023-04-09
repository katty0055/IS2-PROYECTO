from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
<<<<<<< HEAD
from .forms import ProyectoModelForm, UsuarioProyectoFormulario


=======
from .forms import ProyectoUsuarioModelForm, UsuarioProyectoFormulario, UserModelForm
#from usuario_proyecto.models import UsuarioProyecto
from .models import UsuarioProyecto
>>>>>>> 5be894e3ccf15ee9fa5f2ecbd8fdb9a0cec7bedd

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

<<<<<<< HEAD

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
   
=======

def crear_proyecto (request):
    #proyecto_usuario=UsuarioProyectoFormulario(request.POST or None)
    #context={"proyecto_usuario":proyecto_usuario}
    usuario=UsuarioProyecto.objects.all()
    context={"usuario":usuario}
    return render(request,"crear_proyecto.html",context)


>>>>>>> 5be894e3ccf15ee9fa5f2ecbd8fdb9a0cec7bedd
def agregar_usuario(request):
    form_usuario=UsuarioProyectoFormulario(request or None)

<<<<<<< HEAD
    if form_usuario.is_valid():
       print("valido")
       instancia2=form_usuario.save(commit=False)
       instancia.backlog_id='12345'
       instancia=form_usuario.save()

    else:
       form_usuario=UsuarioProyectoFormulario(request or None)

    context={'form_usuario':form_usuario}

    return render(request, 'crear_proyecto2.html', context)
=======

def agregar_registro(request):
    usuario=request.POST['Usuario']
    rol=request.POST['Rol']
    usuario_proyecto=UsuarioProyecto()
>>>>>>> 5be894e3ccf15ee9fa5f2ecbd8fdb9a0cec7bedd


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

