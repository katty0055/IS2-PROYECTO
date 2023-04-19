from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm
from . import models
from django.core.paginator import Paginator 
from django.http import Http404

import datetime


from .forms import  UsuarioProyectoFormulario, UserModelForm, ProyectoFormModel
#from usuario_proyecto.models import UsuarioProyecto
from .models import UsuarioProyecto

# Create your views here.

def  listar_proyectos(request):
    nombre = "Proyecto Scrum"
    proyectos = models.Proyecto.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator= Paginator(proyectos,8)
        proyectos= paginator.page(page)
    except:
        raise Http404
    context = {
        'entity': proyectos,
        'paginator': paginator,
        "nombre": nombre,
    }
    return render(request, "listar_proyectos.html",context)


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


def inicio(request): 
    saludo = "Bienvenido %s" %(request.user)
    nombre = "Proyecto Scrum"
    context ={
        "nombre": nombre,
        "saludo": saludo,
    }
    return render(request,"inicio.html",context)


def cerrar(request):
    logout(request)
    return redirect('login')


def crear_proyecto(request):
    saludo = "Bienvenido %s" %(request.user)
    nombre = "Proyecto Scrum"
    backlog_id_p= "0" +str(models.Proyecto.objects.count())
    if request.method=='POST':
        nombre_p=request.POST['nombre']
        fecha_inicio_p=request.POST['fecha_inicio']
        fecha_fin_p=request.POST['fecha_fin']
        if fecha_inicio_p >= fecha_fin_p:
             messages.error (request, "Fecha de inicio menor o igual que fecha fin, "
                             +"ingrese de vuelta los datos del proyecto")
        else:
            obj= models.Proyecto.objects.create(
                                                backlog_id= backlog_id_p,
                                                nombre=nombre_p,
                                                fecha_inicio=fecha_inicio_p,
                                                fecha_fin= fecha_fin_p)
            return redirect('agregar_usuario_proyecto',pk=obj.backlog_id)
    context ={
        "nombre": nombre,
        "saludo": saludo,
    }
    return render(request, 'crear_proyecto.html',context)


def agregar_usuario_proyecto(request,pk):
    saludo = "Bienvenido %s" %(request.user)
    nombre = "Proyecto Scrum"
    usuarios_eliminados=request.POST.getlist('id_user')
    proyecto= models.Proyecto.objects.get(backlog_id= pk)
    lista_usuarios= models.UsuarioProyecto.objects.filter(backlog_id= pk)
    form_usuario= UsuarioProyectoModelForm(request.POST or None)  
    scrum_master= models.Group.objects.get(name="Scrum Master") 
    product_owner= models.Group.objects.get(name="Product Owner") 
    if form_usuario.is_valid():
        instancia=form_usuario.save(commit=False)
        instancia.backlog_id= pk  
        if lista_usuarios.count()==9:
            messages.error (request, "Miembros llenos, no es posible asociar")
        else:  
            if models.UsuarioProyecto.objects.filter(backlog_id=pk,id_user=instancia.id_user).exists(): 
                messages.error (request, "El usuario ya forma parte de este proyecto, no es posible asociar")     
            elif (lista_usuarios.filter(id_group=product_owner.id).count()==1) and (str(instancia.id_group)==product_owner.name):   
                messages.error (request, "Ya existe un rol Product Owner, no es posible asociar")  
            elif (lista_usuarios.filter(id_group=scrum_master.id).count()==1) and (str(instancia.id_group)== scrum_master.name):   
                messages.error (request, "Ya existe un rol Scrum Master, no es posible asociar")     
            else:
                instancia=form_usuario.save()
        return redirect('agregar_usuario_proyecto',pk=pk)
    for u in usuarios_eliminados:
        lista_usuarios.filter(id_usu_proy_rol=u).delete()    
    context={
        "form_usuario":form_usuario,
        "lista": lista_usuarios,
        "proyecto": proyecto,
        "nombre": nombre,
        "saludo": saludo,
    }
    return render(request, 'agregar_usuario.html', context)


def modificar_proyecto(request,pk): 
    print(type(pk))
    print(pk)
    # proyecto= models.Proyecto.objects.get(backlog_id= pk)
    # usuarios_eliminados=request.POST.getlist('id_user')
    # lista_usuarios= models.UsuarioProyecto.objects.filter(backlog_id= pk)
    # form_usuario=UsuarioProyectoModelForm(request.POST or None)
    # if request.method=='POST':
    #     nombre_nuevo=request.POST['nombre_nuevo']
    #     fecha_inicio_nuevo=request.POST['fecha_inicio_nuevo']
    #     fecha_fin_nuevo=request.POST['fecha_fin_nuevo']  
    #     if fecha_inicio_nuevo >= fecha_fin_nuevo:
    #         messages.error (request, "Fecha de inicio menor o igual que la fecha fin, "
    #                             +"ingrese de vuelta") 
    #     else:  
    #         models.Proyecto.objects.filter(backlog_id= pk).update(
    #                                                     nombre=nombre_nuevo,
    #                                                     fecha_inicio=fecha_inicio_nuevo,
    #                                                     fecha_fin= fecha_fin_nuevo)   
    #     if form_usuario.is_valid():
    #             instancia=form_usuario.save(commit=False)
    #             instancia.backlog_id= pk
    #             if models.UsuarioProyecto.objects.filter(backlog_id=pk,id_user=instancia.id_user).exists():
    #                 messages.error (request, "El usuario ya forma parte de este proyecto, no es posible asociar")    
    #             else:
    #                 instancia=form_usuario.save()
    #                 print(lista_usuarios)
    #                 print(models.UsuarioProyecto.objects.filter(backlog_id= pk))
    #             return redirect('modificar_proyecto',pk=pk)
    #     for u in usuarios_eliminados:
    #             print(lista_usuarios.filter(id_usu_proy_rol=u).delete())
    # context={
    #         "form_usuario":form_usuario,
    #         "lista": lista_usuarios,
    #         "proyecto": proyecto,
    #     }           
    return render(request, 'modificar_proyecto.html', {})






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


<<<<<<< HEAD
def crear_sprint_proyecto(request):
    
    render(request,"crear_sprint_proyecto.html")
=======
>>>>>>> ccae7a61979cfb081a87220231ddad295bede0ab
