from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import ProyectoModelForm, UsuarioProyectoFormulario



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
    return render(request,"inicio.html",{})

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
    print("hola")
    if request.method=='POST':
        username=request.POST['usuario']
        first_name=request.POST['nombre']
        last_name=request.POST['apellido']
        email=request.POST['correo']
        password=request.POST['contrasenha']
        is_active=True
        is_staff=False
        is_superuser=False
        reingresar_contrasenha=request.POST['reingresar_contrasenha']
        date_joined=timezone.now()
        print(username)
        obj=User.objects.create(username=username, first_name=first_name, last_name=last_name,
                                email=email, password=password, is_active=is_active, is_staff=is_staff,
                                is_superuser=is_superuser, date_joined=date_joined)
        obj.save()

    #form=request.POST('formulario')
    #print(form)
    # if request.method=='POST':
    #     print("hola2")
    #     username=request.POST['usuario']
    #     first_name=request.POST['nombre']
    #     last_name=request.POST['apellido']
    #     email=request.POST['correo']
    #     password=request.POST['contrasenha']
    #     is_active=True
    #     is_staff=False
    #     is_superuser=False
    #     reingresar_contrasenha=request.POST['reingresar_contrasenha']
    #     if check_password(reingresar_contrasenha, password):
    #         print("Coinciden")
    #     else: 
    #         messages.error (request, "La contraseña no coincide")
    #     obj=User()
    #     obj.username=username
    #     obj.first_name=first_name
    #     obj.last_name=last_name
    #     obj.email=email
    #     obj.password=password
    #     obj.is_active=is_active
    #     obj.is_staff=is_staff
    #     obj.is_superuser=is_superuser
    #     obj.date_joined=timezone.now()
    #     obj.save()
    #     print(obj)
    return render(request,"crear_usuarios.html",{})

