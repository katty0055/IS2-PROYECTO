from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .forms import ProyectoModelForm,  UsuarioProyectoModelForm, UserModelForm, UserProfileModelForm, UserPasswordModelForm, UserStoryModelForm, UserStoryCreacionModelForm, SprintModelForm, UserStoryEliminarModelForm, ComentarioUserStoryModelForm
from django.db.models import Q
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
from datetime import datetime,date
from .models import UsuarioProyecto, Sprint, EstadosUserStory, ComentariosUserStory
import matplotlib.pyplot
import numpy
import io
import urllib, base64

# from .forms import SelectUserModelForm

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
            tareas=models.UserStory.objects.filter(id_usu_proy_rol__backlog=pk, id_usu_proy_rol=u)
            print(tareas)
            if len(tareas)>0:
                print(models.UsuarioProyecto.objects.filter(backlog_id= pk,id_group=models.Group.objects.get(name="Creador")))
                creador=models.UsuarioProyecto.objects.get(backlog_id= pk,id_group=models.Group.objects.get(name="Creador"))
                tareas.update(id_usu_proy_rol=creador)
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
        nombreform=request.POST['nombre']
        proyecto=models.Proyecto.objects.get(backlog_id=pk)
        print(proyecto.backlog_id)
        if fecha_inicioform == "":
            messages.error(request,"Favor ingrese una fecha de inicio")
        else:
            
            obj= models.Sprint.objects.create(
                                                nombre= nombreform,
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

def listar_sprint_proyecto(request):
    nombre = "Proyecto Scrum"
    sprints = Sprint.objects.all()
    #proyectos = models.UsuarioProyecto.objects.filter(id_user=request.user).distinct('backlog')
    page = request.GET.get('page',1)
    try:
        paginator= Paginator(sprints,8)
        sprints= paginator.page(page)
    except:
        raise Http404
    context = {
        'entity': sprints,
        'paginator': paginator,
        "nombre": nombre,
    }
    return render(request, "listar_sprint_proyecto.html",context)

def modificar_sprint_proyecto(request,pk):
    nombre = "Proyecto Scrum"
    sprint_proyecto=models.Sprint.objects.get(backlog_id_sprint=pk)
    #form=SprintModelForm(data=request.POST or None, instance=sprint_proyecto)

    if request.method == "POST":
        fecha_inicioform=request.POST['fecha_inicio']
        fecha_finform=request.POST['fecha_fin']
        nombre_s= nombreform=request.POST['nombre']
        if fecha_inicioform == "":
            messages.error(request,"Favor ingrese una fecha de inicio")
        else:
            
            models.Sprint.objects.filter(backlog_id_sprint=pk).update(
                                            fecha_inicio = fecha_inicioform,
                                            fecha_fin = fecha_finform,
                                            nombre=nombre_s
                                        )
            messages.success(request,"Sprint Modificado con exito")
            print(pk)
            return redirect('backlog',pk=sprint_proyecto.backlog_id)


    context = {
        "sprint":sprint_proyecto,
        "pk": pk,
    }
    return render(request,"modificar_sprint_proyecto.html",context)

'''def crear_user_story(request,pk):
    # print(pk)
    form= UserStoryCreacionModelForm(request.POST or None)
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
    return render(request,"crear_us.html",context)'''

def crear_user_story(request,pk):
    # print(pk)
    form= UserStoryCreacionModelForm(request.POST or None)
    proyecto=models.Proyecto.objects.get(backlog_id=pk)
    fecha_inicio_proyecto=proyecto.fecha_inicio
    fecha_fin_proyecto=proyecto.fecha_fin
    if form.is_valid():
        instance= form.save(commit=False)
        id_usu_proy_rol=models.UsuarioProyecto.objects.filter(backlog=pk,id_user=request.user).first()
        instance.id_usu_proy_rol=id_usu_proy_rol
        #Fecha Inicio y Fecha Fin: estas fechas deben estar comprendidas dentro del periodo de duración previsto del proyecto.
        if instance.fecha_inicio < fecha_inicio_proyecto or instance.fecha_inicio > fecha_fin_proyecto:
            messages.error(request,"Favor ingrese una fecha de inicio dentro de la duracion del proyecto" +" "+str(fecha_inicio_proyecto)+"/"+str(fecha_fin_proyecto))
        elif instance.fecha_fin > fecha_fin_proyecto or instance.fecha_fin < fecha_inicio_proyecto:
             messages.error(request,"Favor ingrese una fecha de finalizacion dentro de la duracion del proyecto" +" "+str(fecha_inicio_proyecto)+"/"+str(fecha_fin_proyecto))
        else:
            
            instance = form.save()
            form= UserStoryModelForm() #Blanquea el formulario
            messages.success(request,"US creado con exito")
            return redirect('agregar_comentario_us', instance.id_user_story, pk)
    context = {
        "form": form,
        "pk": pk,
    }
    return render(request,"crear_us.html",context)


def editar_user_story(request,pk):
    cerrado=True
    sum=0
    nombre = "Proyecto Scrum"
    user_story=models.UserStory.objects.get(id_user_story=pk)
    us=user_story.id_estado
    form_comentario=ComentarioUserStoryModelForm(request.POST or None)
    id_proyecto=user_story.id_usu_proy_rol.backlog
    usuarios=models.UsuarioProyecto.objects.filter(backlog= id_proyecto)
    if ((user_story.id_usu_proy_rol.id_user.username==str(request.user) and
        user_story.id_usu_proy_rol.id_group.name!="Creador")
        or usuarios.filter(
        id_user__username= str(request.user), id_group__name="Scrum Master").exists()):
        if request.method == "POST":
            form = UserStoryModelForm(request.POST, instance = user_story)
            nueva_fecha_fin=request.POST.get('fecha_fin_nuevo')
            nueva_fecha_inicio=request.POST.get('fecha_inicio_nuevo')  
            if form.is_valid():
                        instance = form.save(commit=False)
                        print(us)
                        print(user_story.id_estado)
                        print(instance.id_estado)
                        if us!=instance.id_estado:
                            print("validar usuario")
                            print((str(instance.id_estado)))
                            print((str(models.EstadosUserStory.objects.get(nombre_estado='Doing').id_estado)))
                            if str(instance.id_estado)==str(models.EstadosUserStory.objects.get(nombre_estado='Doing'
                                ).nombre_estado) or str(instance.id_estado)==str(models.EstadosUserStory.objects.get(nombre_estado='Done').nombre_estado):
                               print("Que pasa")
                               if user_story.id_usu_proy_rol.id_group.name=="Creador":
                                   messages.error(request,'No hay usuario asignado, NO se puede cambiar el estado')
                                   return redirect('modificar_user_story',pk=user_story.id_user_story)
                                 
                        if nueva_fecha_inicio !="":
                            instance.fecha_inicio= nueva_fecha_inicio
                        if nueva_fecha_fin != "":
                            instance.fecha_fin= nueva_fecha_fin
                        messages.success(request, 'US Actualizado !!')
                        instance.save()
                        sprints= models.Sprint.objects.filter(backlog_id=id_proyecto)
                        ultima_sprint=sprints.filter(fecha_fin_real=None, estado=True)
                        if ultima_sprint.count()==1:
                            if user_story.backlog_id_sprint == ultima_sprint.get():
                                cerrado==True
                            user_stories=models.UserStory.objects.filter(id_usu_proy_rol__backlog_id=id_proyecto)
                            for u in user_stories:
                                if u.id_estado.descripcion =="ToDo" or u.id_estado.descripcion =="Doing":
                                    print("false")
                                    cerrado=False
                            if cerrado==True:
                                print("cambio")
                                models.Proyecto.objects.filter(backlog_id=id_proyecto).update(fecha_fin_real=timezone.now())
                        
                        if form_comentario.is_valid():
                            print("comentario valido=)")
                            instancia=form_comentario.save(commit=False)
                            #si es que no se ingreso ningun comentario
                            print((instancia.comentario))
                            if instancia.comentario== None:
                                 messages.error(request, 'No se ha asignado ningun comentario')
                            else:
                                comentarios=models.ComentariosUserStory.objects.all()
                                print(comentarios)
                                longitud=len(comentarios)
                                print(longitud)
                                instancia=form_comentario.save()
                                models.ComentariosUserStory.objects.filter(id_comentario=longitud+1).update(us=user_story)
                                messages.success(request, 'Se ha guardado el comentario')
                        return redirect('modificar_user_story',pk=user_story.id_user_story)
                        #return redirect('backlog',pk=user_story.id_usu_proy_rol.backlog)
        else:  
            form = UserStoryModelForm(instance = user_story)
        context = {"form":form, "us": user_story, "form_comentario": form_comentario}       
        return render(request,'modificar_user_story.html',context)
    else:
        messages.error(request,"No es el Scrum Master o usuario asignado a la tarea")
        return redirect('backlog',pk=user_story.id_usu_proy_rol.backlog)

def agregar_comentario_us(request, id, pk):
    nombre = "Proyecto Scrum"
    #sprint = models.Sprint.objects.get(backlog_id_sprint= pk)
    user_story=models.UserStory.objects.get(id_user_story=id)
    #user_story=models.UserStory.objects.filter(backlog_id_sprint=pk, id_user_story=id)
    form_comentario= ComentarioUserStoryModelForm(request.POST or None)
    if form_comentario.is_valid():
        print("valido=)")
        instancia=form_comentario.save(commit=False)
        #si es que no se ingreso ningun comentario
        print((instancia.comentario))
        if instancia.comentario== None:
            messages.error(request, 'No se ha asignado ningun comentario')
        else:
            comentarios=models.ComentariosUserStory.objects.all()
            print(comentarios)
            longitud=len(comentarios)
            print(longitud)
            instancia=form_comentario.save()
            models.ComentariosUserStory.objects.filter(id_comentario=longitud+1).update(us=user_story)
                    
            messages.success(request, 'Se ha guardado el comentario')
    
    context={ "form_comentario":form_comentario,
        "user_story": user_story,
        "nombre": nombre,
        }
    
    return render(request, 'agregar_comentario.html', context) 

def  listar_us(request):
    nombre = "Proyecto Scrum"
    proyectos = models.UserStory.objects.all()
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
    return render(request, "listar_us.html",context)


def backlog(request, pk):
    print(pk)
    
    nombre = "Proyecto Scrum"
    us = models.UserStory.objects.filter(id_usu_proy_rol__backlog=pk)
    sprint = models.Sprint.objects.filter(backlog_id=pk,estado=True)
    user= models.UsuarioProyecto.objects.filter(backlog_id=pk).exclude(id_group__name="Creador")
    if request.method == "POST":
        if 'cambiar' in request.POST:
            tarea_id=request.POST['item']
            print("cambai")
            print(tarea_id)
            print(models.UserStory.objects.get(id_user_story=tarea_id))
            creador=models.UsuarioProyecto.objects.get(backlog_id= pk,id_group=models.Group.objects.get(name="Creador"))
            print(creador)
            models.UserStory.objects.filter(id_user_story=tarea_id).update(id_usu_proy_rol=creador)
        elif 'miboton' in request.POST:
            usuario=request.POST.get('user')
            id_us=request.POST.get('id')
            print(usuario)
            print(id_us)
            if usuario != "---":
                us.filter(id_user_story= id_us).update(id_usu_proy_rol= user.get(id_user__username= usuario))
            else:
                redirect('backlog',pk=pk)
      
            

    context ={
        "nombre": nombre,
        "us": us,
        "user":user,
        "sprint":sprint,


    }
    return render(request, "backlog.html",context)


def eliminar_sprint(request, pk):
    nombre = "Proyecto Scrum"
    sprint = models.Sprint.objects.get(backlog_id_sprint= pk)
    #recupera los datos del formulario del sprint asociada a la pk
    form = SprintModelForm(data=request.POST or None, instance=sprint)
   
    if request.method == 'POST':
        #cambia el estado del proyecto de True a False
        #models.Proyecto.objects.filter(backlog_id= pk).update(estado=False)
        sprint.estado = False
        sprint.save()
        messages.success(request, 'El sprint ha sido borrado con exito')
        return redirect('backlog',pk=sprint.backlog_id)
    
    context = {"form":form, "nombre":nombre, "backlog_id":sprint.backlog_id}
    return render(request, 'eliminar_sprint.html', context)


def eliminar_user_story(request, pk):
    nombre = "Proyecto Scrum"
    user_story= models.UserStory.objects.get(id_user_story= pk)
    #recupera los datos del formulario de la user story asociada a la pk
    form = UserStoryEliminarModelForm(data=request.POST or None, instance=user_story)
   
    if request.method == 'POST':
        #cambia el estado del proyecto de True a False
        #models.Proyecto.objects.filter(backlog_id= pk).update(estado=False)
        user_story.id_estado= models.EstadosUserStory.objects.get(descripcion= "Cancelled")
        user_story.save()
        messages.success(request, 'La user story ha sido cancelada con exito')
        return redirect('backlog',pk=user_story.id_usu_proy_rol.backlog)
    
    context = {"form":form, "nombre":nombre, }
    return render(request, 'eliminar_us.html', context)


def asignar_us_a_sprint(request,pk): 
    nombre = "Proyecto Scrum"
    sprint= models.Sprint.objects.get(backlog_id_sprint= pk) 
    us_seleccionados=request.POST.getlist('id_us')
    lista_user_story= models.UserStory.objects.filter(id_usu_proy_rol__backlog = sprint.backlog_id, backlog_id_sprint=None)
    us_sprint= models.UserStory.objects.filter(backlog_id_sprint  = pk)
    if request.method=='POST':
        if 'miboton' in request.POST:
            for us in us_seleccionados:
                models.UserStory.objects.filter(id_user_story= us).update(
                backlog_id_sprint=sprint) 
        elif 'delete' in request.POST:
            us_sacar=request.POST['item']
            models.UserStory.objects.filter(id_user_story= us_sacar).update(
                backlog_id_sprint=None) 
    context={
            "lista": lista_user_story,
            "sprint": sprint,
            "nombre": nombre,
            "us_sprint": us_sprint,
        }           
    return render(request,'asignar_us.html', context)

def iniciar_cerrar_sprint(request, pk, accion):
    print(type(pk))
    sprint=models.Sprint.objects.get(backlog_id_sprint=pk)
    sprints= models.Sprint.objects.filter(backlog_id=sprint.backlog_id)
    us_sprint=models.UserStory.objects.filter(id_usu_proy_rol__backlog = sprint.backlog_id)
    print("--")
    print(us_sprint)
    print("--")
    #us_sprint=models.UserStory.objects.get(backlog_id_sprint=sprint.backlog_id_sprint)
    #us_sprint2=models.UserStory.objects.filter(id_user_story=us_sprint.id_user_story)
    #backlog_id_sprint=us_sprint.backlog_id_sprint,id_usu_proy_rol__backlog = sprint.backlog_id
    #us_sprint= models.UserStory.objects.filter(backlog_id_sprint  = pk)
    #estados=models.EstadosUserStory.objects.filter(id_estado)
    
    activo_sprint=False
    cerrado=False
    for s in sprints:
        print(type(s.backlog_id_sprint))
        if s.fecha_inicio_real !=None:
            print("fecha_inicio activo")
            if s.fecha_fin_real==None and accion=="Iniciar":
                print("que")
                activo_sprint=True
            elif accion=="Cerrar" and s.backlog_id_sprint==int(pk):        
                print("hola")       
                sprint.fecha_fin_real= timezone.now()
                sprint.save()
                cerrado=True
     

    if activo_sprint:
        messages.error(request,"No se puede iniciar el Sprint porque otro esta activo")
    elif accion=="Iniciar":
        #ids=models.UserStory.objects.values_list("backlog_id_sprint", flat=True).distinct()
        #for i in ids:
            #print(i)
        bandera = 0
        for lista in us_sprint:
            if lista.backlog_id_sprint is not None and lista.backlog_id_sprint.backlog_id_sprint==sprint.backlog_id_sprint:
                bandera += 1
        #No se debe poder iniciar un Sprint cuyo Sprint Backlog no esté asociado a US caso contrario se inicia el Sprint
        if bandera == 0:
            messages.error(request,"No se puede iniciar el Sprint porque no esta asociado a un User Story")
        else: 
            messages.success(request,"Sprint Iniciado")
            sprint.fecha_inicio_real= timezone.now()
            sprint.save()
            if sprints.exclude(fecha_inicio_real= None).count() == 1:
                models.Proyecto.objects.filter(backlog_id=sprint.backlog_id).update(fecha_inicio_real=timezone.now())
    
    if cerrado:
        print("-------------")
        print("Hola Man")
        print("--------------")
        contador=0 #cuenta cuantos us No estan en Done
        contador2=0 #cuenta cuantos us estan en Done
        #verifica si todas las us de un sprint estan en Done
        for lista in us_sprint:
            if lista.id_estado == "Done" and lista.backlog_id_sprint.backlog_id_sprint == sprint.backlog_id_sprint:
                contador2+=1
            else:
                contador+=1
        #Una vez que todas las US de un Sprint están en Done, se puede cerrar el Sprint.
        if contador2 > 0 and contador==0:
            messages.success(request,"Sprint Cerrado")
        elif contador2==0 and contador>0:
            messages.error(request, "NO se puede cerrar el Sprint porque la(s) US del Sprint NO esta(n) en el estado Done")
       
    elif accion=="Cerrar":
        print("-------------")
        print("Hola Men")
        print("--------------")
        #if accion=="Cerrar" and activo_sprint==False:
        messages.error(request,"No se puede cerrar el Sprint porque no esta activo")
       
    return redirect('backlog',pk=sprint.backlog_id)


def ver_kanban(request,pk): 
    nombre = "Proyecto Scrum"
    user_stories_toDo=models.UserStory.objects.filter(
        id_usu_proy_rol__backlog_id=pk,id_estado__descripcion="ToDo")
    user_stories_doing=models.UserStory.objects.filter(
        id_usu_proy_rol__backlog_id=pk,id_estado__descripcion="Doing")
    user_stories_done=models.UserStory.objects.filter(
        id_usu_proy_rol__backlog_id=pk,id_estado__descripcion="Done")
    print(user_stories_done)
    context={           
        "nombre": nombre,  
        "user_stories_toDo": user_stories_toDo,  
        "user_stories_doing": user_stories_doing,
        "user_stories_done": user_stories_done,      
    }           
    return render(request,'kanban.html', context)

def burndown_chart(request,pk):
    nombre = "Proyecto Scrum"
    # matplotlib.pyplot.style.use('_mpl-gallery')

    # # make data
    # numpy.random.seed(3)
    # x = 0.5 + numpy.arange(8)
    # y = numpy.random.uniform(2, 7, len(x))

    # # plot
    # fig, ax = matplotlib.pyplot.subplots()

    # ax.step(x, y, linewidth=2.5)

    # ax.set(xlim=(0, 8), xticks=numpy.arange(1, 8),
    #     ylim=(0, 8), yticks=numpy.arange(1, 8))

    # matplotlib.pyplot.show()
    x = numpy.arange(0, 5, 1)
    y = numpy.sin(x)
    matplotlib.pyplot.plot(x, y)
    fig= matplotlib.pyplot.gcf()
    buf=io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    context={           
        "nombre": nombre,  
        "data":uri,
            
    }           
    return render(request,'burndown_chart.html', context)

