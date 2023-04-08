from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import ProyectoUsuarioModelForm, UsuarioProyectoFormulario, UserModelForm
#from usuario_proyecto.models import UsuarioProyecto
from .models import UsuarioProyecto

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


def crear_proyecto (request):
    #proyecto_usuario=UsuarioProyectoFormulario(request.POST or None)
    #context={"proyecto_usuario":proyecto_usuario}
    usuario=UsuarioProyecto.objects.all()
    context={"usuario":usuario}
    return render(request,"crear_proyecto.html",context)


def agregar_usuario(request):
    return render(request,'agregar_usuario.html')


def agregar_registro(request):
    usuario=request.POST['Usuario']
    rol=request.POST['Rol']
    usuario_proyecto=UsuarioProyecto()


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

