from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

    

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

def crear_usuario(request):
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
        if check_password(reingresar_contrasenha, password):
            print("Coinciden")
        else: 
            messages.error (request, "La contraseña no coincide")
        obj=User()
        obj.username=username
        obj.first_name=first_name
        obj.last_name=last_name
        obj.email=email
        obj.password=password
        obj.is_active=is_active
        obj.is_staff=is_staff
        obj.is_superuser=is_superuser
        print(obj)
    return render(request,"crear_usuarios.html",{})
