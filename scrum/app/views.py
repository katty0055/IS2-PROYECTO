from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, UserPasswordModelForm, UserStoryModelForm
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, UserPasswordModelForm
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, UserStoryModelForm
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, UserStoryModelForm
from .forms import ProyectoModelForm, UsuarioProyectoFormulario, UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, Proyecto
from django.db.models import Q
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime


from .forms import  UsuarioProyectoFormulario, UserModelForm, ProyectoFormModel
#from usuario_proyecto.models import UsuarioProyecto
from .models import UsuarioProyecto

# Create your views here.

'''def  listar_proyectos(request):
    nombre = "Proyecto Scrum"
    proyectos = models.Proyecto.objects.all()
    proyectos_activos = []
    
    for proyecto in proyectos:
        if proyecto.estado:
            proyectos_activos.append(proyecto)
    
    page = request.GET.get('page',1)
    try:
        paginator= Paginator(proyectos,8)
        proyectos_activos= paginator.page(page)
    except:
        raise Http404
    context = {
        'entity': proyectos_activos,
        'paginator': paginator,
        "nombre": nombre,
    }
    return render(request, "listar_proyectos.html",context)'''

def  listar_proyectos(request):
    nombre = "Proyecto Scrum"
    # proyectos = models.Proyecto.objects.all()
    proyectos = models.UsuarioProyecto.objects.filter(id_user=request.user).distinct('backlog')
    # me trae los distontos proyectos a los que esta asociado un usuario
    proyectos_activos = []
    solicitud_busqueda = request.GET.get("buscar")

    if solicitud_busqueda:
        # proyectos = models.Proyecto.objects.filter(
        #     #Q revisa el o los campos del modelo (en este caso campos del Proyecto)
        #     #icontains hace que no sea exacto la busqueda, ejemplo: si se recibe "scrum", en la base de datos podria estar asi "Scrum"
        #     Q(nombre__icontains = solicitud_busqueda) |
        #     Q(fecha_inicio__icontains = solicitud_busqueda)
        # ).distinct() #se usa distinct para el caso de que haya coincidencias
        proyectos = proyectos.filter(
             Q(backlog__nombre__icontains = solicitud_busqueda) |
             Q(backlog__fecha_inicio__icontains = solicitud_busqueda)
        ).distinct()
   
    for proyecto in proyectos:
        if proyecto.backlog.estado: #proyectos almacena la tabla usuarioProyecto, desde esa tabla accedo por la relacion a la tabla proyectos a traves de backlog y luego el estado
            proyectos_activos.append(proyecto)
   
    page = request.GET.get('page',1)
    
    try:
        paginator= Paginator(proyectos_activos,8)
        proyectos_activos= paginator.page(page)
    #except PageNotAnInteger:
        #proyectos_activos = paginator.page(1)
    #except EmptyPage:
        #proyectos_activos = paginator.page(paginator.num_pages)
    except:
        raise Http404
    
    context = {
        'entity': proyectos_activos,
        "nombre": nombre,
        'paginator':paginator,
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
            models.UsuarioProyecto.objects.create(
                                                backlog_id= backlog_id_p,
                                                id_user=request.user,
                                                id_group=models.Group.objects.get(name="Creador"),   
            )
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
    lista_usuarios= models.UsuarioProyecto.objects.filter(backlog_id= pk).exclude(id_group=models.Group.objects.get(name="Creador"))
    form_usuario= UsuarioProyectoModelForm(request.POST or None)  
    scrum_master= models.Group.objects.get(name="Scrum Master") 
    product_owner= models.Group.objects.get(name="Product Owner") 
    if form_usuario.is_valid():
        instancia=form_usuario.save(commit=False)
        instancia.backlog_id= pk  
        if lista_usuarios.count()==10:
            messages.error (request, "Miembros llenos, no es posible asociar")
        else:  
            usuarios_seleccionados=models.UsuarioProyecto.objects.filter(backlog_id=pk).exclude(id_group=models.Group.objects.get(name="Creador"))
            print(usuarios_seleccionados.filter(id_user=instancia.id_user))
            if usuarios_seleccionados.filter(id_user=instancia.id_user).exists(): 
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
    nombre = "Proyecto Scrum"
    usuarios_eliminados=request.POST.getlist('id_user')
    lista_usuarios= models.UsuarioProyecto.objects.filter(backlog_id= pk).exclude(id_group=models.Group.objects.get(name="Creador"))
    form_usuario=UsuarioProyectoModelForm(request.POST or None)
    scrum_master= models.Group.objects.get(name="Scrum Master") 
    product_owner= models.Group.objects.get(name="Product Owner") 


    # proyecto= models.Proyecto.objects.get(backlog_id= pk) 
    # form_proyecto = ProyectoModelForm(request.POST,instance=proyecto)
    if request.method=='POST':
        nombre_nuevo=request.POST.get('nombre_nuevo', False)
        fecha_inicio_nuevo=request.POST.get('fecha_inicio_nuevo', False)
        fecha_fin_nuevo=request.POST.get('fecha_fin_nuevo', False)# Se usa get para evitar un error en caso que no se modifique la fecha
        if fecha_fin_nuevo != False or  fecha_inicio_nuevo != False:#Solo entra si uno de los valores cambio
            if fecha_inicio_nuevo >= fecha_fin_nuevo:
                messages.error (request, "Fecha de inicio mayor o igual que la fecha fin, "
                                    +"ingrese de vuelta") 
            else:  
                models.Proyecto.objects.filter(backlog_id= pk).update(
                                                            nombre=nombre_nuevo,
                                                            fecha_inicio=fecha_inicio_nuevo,
                                                            fecha_fin= fecha_fin_nuevo)   
        if form_usuario.is_valid():
            instancia=form_usuario.save(commit=False)
            instancia.backlog_id= pk  
            if lista_usuarios.count()==10:
                messages.error (request, "Miembros llenos, no es posible asociar")
            else:  
                usuarios_seleccionados=models.UsuarioProyecto.objects.filter(backlog_id=pk).exclude(id_group=models.Group.objects.get(name="Creador"))
                print(usuarios_seleccionados.filter(id_user=instancia.id_user))
                if usuarios_seleccionados.filter(id_user=instancia.id_user).exists(): 
                    messages.error (request, "El usuario ya forma parte de este proyecto, no es posible asociar")     
                elif (lista_usuarios.filter(id_group=product_owner.id).count()==1) and (str(instancia.id_group)==product_owner.name):   
                    messages.error (request, "Ya existe un rol Product Owner, no es posible asociar")  
                elif (lista_usuarios.filter(id_group=scrum_master.id).count()==1) and (str(instancia.id_group)== scrum_master.name):   
                    messages.error (request, "Ya existe un rol Scrum Master, no es posible asociar")     
                else:
                    instancia=form_usuario.save()
            return redirect('modificar_proyecto',pk=pk)
        for u in usuarios_eliminados:
            lista_usuarios.filter(id_usu_proy_rol=u).delete()    

   
    proyecto= models.Proyecto.objects.get(backlog_id= pk) 
    context={
            "form_usuario":form_usuario,
            "lista": lista_usuarios,
            "proyecto": proyecto,
            "nombre": nombre,
            # "form_p": form_proyecto,
            
        }           
    return render(request, 'modificar_proyecto.html', context)


def eliminar_proyecto(request, pk):
    nombre = "Proyecto Scrum"
    proyecto = models.Proyecto.objects.get(backlog_id = pk)
    #recupera los datos del formulario del proyecto asociada a la pk
    form = ProyectoModelForm(data=request.POST or None, instance=proyecto)
   
    if request.method == 'POST':
        #cambia el estado del proyecto de True a False
        #models.Proyecto.objects.filter(backlog_id= pk).update(estado=False)
        proyecto.estado = False
        proyecto.save()
        messages.success(request, 'El proyecto ha sido borrado con exito')
        return redirect("listar_proyectos")
    
    context = {"form":form, "nombre":nombre, "backlog_id":pk}
    return render(request, 'eliminar_proyecto.html', context)



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

@login_required(login_url='login')
def editar_perfil(request):
    nombre = "Proyecto Scrum"
    
    if request.method == "POST":
        form = UserProfileModelForm(data=request.POST or None, instance=request.user)
        if form.is_valid():
            if len(User.objects.filter(email=request.POST['email']).exclude(username=request.POST['username']))>0:
                messages.error(request, 'El email esta registrado a otro usuario')
            else:
                form.save()
                messages.success(request, 'Perfil Actualizado !!')
                return redirect('login')     
    else:
        form = UserProfileModelForm(instance = request.user)
    
    context = {"form":form,
               "nombre": nombre,}
    return render(request,'modificar_usuario.html',context)


@login_required(login_url='login')
def editar_password(request):

    if request.method == "POST":
        form = UserPasswordModelForm(data=request.POST, user=request.user)
        if form.is_valid():
            messages.success(request, 'Contraseña Actualizada !!')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(to='login')
        #else:
            #return redirect('modificar_password')
    else:
        form = UserPasswordModelForm(user=request.user)
    
    context = {"form":form}
    return render(request, 'modificar_password.html', context)


@login_required(login_url='login')
def eliminar_usuario(request):
   
    form = UserProfileModelForm(instance = request.user)
    
    if request.method == 'POST':
        #obtener usuario de inicio de sesion
        user = User.objects.get(username = request.user)
        # Verifique que el usuario de inicio de sesión y el usuario que se va a eliminar sean los mismos
        if request.user == user:
            #cambia el estado del usuario de True a False
            user.is_active = False
            user.save()
            messages.success(request, 'Tu perfil ha sido borrado con exito')
            return redirect("login")
        else:
            messages.error(request, 'No tienes permiso para borrar este perfil')
            return redirect("login")
        
    context ={"form":form}
    return render(request, 'eliminar_usuario.html',context)
   
def crear_sprint_proyecto(request, pk):
    print(pk)
    if request.method=='POST':
        fecha_inicioform=request.POST['fecha_inicio']
        fecha_finform=request.POST['fecha_fin']
        proyecto=models.Proyecto.objects.get(backlog_id=pk)
        print(proyecto.backlog_id)
        if fecha_inicioform == "":
            messages.error(request,"Favor ingrese una fecha de inicio")
        else:
            
            obj= models.Sprint.objects.create(
                                                fecha_inicio = fecha_inicioform,
                                                fecha_fin = fecha_finform,
                                                backlog_id=proyecto
                                            )
            messages.success(request,"Sprint creado con exito")
            return redirect('crear_sprint_proyecto',pk=pk)
    
    context ={
        "pk": pk,
    }
    
    return render(request,'crear_sprint_proyecto.html',context)


def crear_user_story(request,pk):
    # print(pk)
    form= UserStoryModelForm(request.POST or None)
    if form.is_valid():
        instance= form.save(commit=False)
        id_usu_proy_rol=models.UsuarioProyecto.objects.filter(backlog=pk,id_user=request.user).first()
        instance.id_usu_proy_rol=id_usu_proy_rol
        instance = form.save()
        form= UserStoryModelForm() #Blanquea el formulario
        messages.success(request,"US creado con exito")
    context = {
        "form": form,
        "pk": pk,
    }
    return render(request,"crear_us.html",context)