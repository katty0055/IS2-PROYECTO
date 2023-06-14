from django import forms
from .models import Proyecto, UsuarioProyecto, UserStory, EstadosUserStory, Sprint
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.admin import widgets



class ProyectoModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre"].widget.attrs.update({
            'required':'',
            'type':'text',
            'name':'nombre_proyecto',
            'placeholder':'',
            'class':'input input-name'
        })
        self.fields["fecha_inicio"].widget.attrs.update({
            'required':'',
            'type':'date',
            'placeholder':'',
            'class':'input input-date'
        })
        self.fields["fecha_fin"].widget.attrs.update({
            'required':'',
            'type':'date',
            'placeholder':'',
            'class':'input input-date'
        })
     
       
    class Meta:
        model=Proyecto
        fields=["nombre","fecha_fin","fecha_inicio"]


class ProyectoFormModel(forms.ModelForm):  
    class Meta:
        model=Proyecto
        fields=["nombre","fecha_fin","fecha_inicio"]



class UsuarioProyectoModelForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_user"].widget.attrs.update({
            'class':'desplegable '
        })
        self.fields["id_group"].widget.attrs.update({
            'class':'desplegable '
        })
        self.fields["id_group"].queryset=Group.objects.exclude(name="Creador")

    class Meta:
        model=UsuarioProyecto
        fields=["id_user","id_group"]
       

class UsuarioProyectoFormulario(forms.Form):
    usuario=forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(),required=True)
    rol=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(),required=True)



User = get_user_model()
class UserModelForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["first_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["last_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["email"].widget.attrs.update({
            'required': '',
            'type':'email',
            'placeholder':'',
            'class':'input input-email' 
        })
        self.fields["password1"].widget.attrs.update({
            'required': '',
            'type':'password',
            'placeholder':'',
            'class':'input input-password' 
        })
        self.fields["password2"].widget.attrs.update({
            'required': '',
            'type':'password',
            'placeholder':'',
            'class':'input input-password' 
        })
      
    class Meta:
        model= User
        fields=["username","first_name","last_name","email","password1","password2"]


#User = get_user_model()
class UserProfileModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["first_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["last_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name' 
        })
        self.fields["email"].widget.attrs.update({
            'required': '',
            'type':'email',
            'placeholder':'',
            'class':'input input-email' 
        })
        
    class Meta:
        model= User
        fields=["username","first_name","last_name","email"]


class UserPasswordModelForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({
            'required': '',
            'type':'password',
            'placeholder':'',
            'class':'input input-password' 
        })
        self.fields["new_password1"].widget.attrs.update({
            'required': '',
            'type':'password',
            'placeholder':'',
            'class':'input input-password'  
        })
        self.fields["new_password2"].widget.attrs.update({
            'required': '',
            'type':'password',
            'placeholder':'',
            'class':'input input-password'  
        })
    class Meta:
        model= User
        fields=["old_password","new_password1","new_password2"]


##Este es para modificar US, NO BORRAR
class UserStoryModelForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_story_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'nombre',
        })
        self.fields["descripcion"].widget.attrs.update({
            'placeholder':'',
            'class':'input input-description',
            'id': '',
            'name': 'descripcion',
        })
        self.fields["story_points"].widget.attrs.update({
            'type':'number',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'story_points',
        })
        self.fields["id_prioridad"].widget.attrs.update({
            'required': '',
            'class':'input input-prioridad',
            'name': 'prioridad',
        })
        self.fields["id_estado"].widget.attrs.update({
            'required': '',
            'class':'input input-prioridad',
            'name': 'estado',
        })
        self.fields["fecha_inicio"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_inicio',
        })
        self.fields["fecha_fin"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_fin',
        })

        self.fields["definicion_hecho"].widget.attrs.update({
            'required': '',
            'placeholder':'',
            'class':'input input-description',
            'id': 'name',
            'name': 'definicion_hecho',
        })

    class Meta:
        model=UserStory
        fields=["user_story_name","descripcion","story_points","definicion_hecho","id_prioridad","id_estado","fecha_inicio","fecha_fin"]

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'definicion_hecho':forms.Textarea(attrs={'cols': 30, 'rows': 8}),
            'descripcion':forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }
#Creacion de US
class UserStoryCreacionModelForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_story_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'nombre',
        })
        self.fields["descripcion"].widget.attrs.update({
            'placeholder':'',
            'class':'input input-description',
            'id': '',
            'name': 'descripcion',
        })
        self.fields["story_points"].widget.attrs.update({
            'type':'number',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'story_points',
        })
        self.fields["id_prioridad"].widget.attrs.update({
            'required': '',
            'class':'input input-prioridad',
            'name': 'prioridad',
        })
        self.fields["id_estado"].widget.attrs.update({
            'required': '',
            'class':'input input-prioridad',
            'name': 'estado',
        })
        self.fields["fecha_inicio"].widget.attrs.update({
            'required': '',
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_inicio',
        })
        self.fields["fecha_fin"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_fin',
        })

        self.fields["definicion_hecho"].widget.attrs.update({
            'required': '',
            'placeholder':'',
            'class':'input input-description',
            'id': 'name',
            'name': 'definicion_hecho',
        })

        self.fields["id_estado"].queryset=EstadosUserStory.objects.filter(nombre_estado="ToDo") 

    class Meta:
        model=UserStory
        fields=["user_story_name","descripcion","story_points","definicion_hecho","id_prioridad","id_estado","fecha_inicio","fecha_fin"]

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'definicion_hecho':forms.Textarea(attrs={'cols': 30, 'rows': 8}),
            'descripcion':forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }

class SprintModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["backlog_id"].widget.attrs.update({
            'type':'name',
            'placeholder':'',
            'class':'input ',
            'name': 'backlog_id',
        })
        self.fields["fecha_inicio"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input' ,
            'name': 'fecha_inicio',
        })
        self.fields["fecha_fin"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input ',
            'name': 'fecha_fin',
        })
        self.fields["fecha_inicio_real"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input ',
            'name': 'fecha_inicio_real',
        })
        self.fields["fecha_fin_real"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input ',
            'name': 'fecha_fin_real',
        })
        self.fields["nombre"].widget.attrs.update({
            'type':'text',
            'placeholder':'',
            'class':'input ',
            'name': 'nombre',
        })
    class Meta:
        model=Sprint
        fields=["backlog_id","fecha_inicio","fecha_fin","fecha_inicio_real","fecha_fin_real","nombre"]




##Este es para borrar US, NO BORRAR porfavoor
class UserStoryEliminarModelForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_story_name"].widget.attrs.update({
            'required': '',
            'type':'text',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'nombre',
            'readonly':'readonly',
        })
        self.fields["descripcion"].widget.attrs.update({
            'placeholder':'',
            'class':'input input-description',
            'id': '',
            'name': 'descripcion',
            'readonly':'readonly',
        })
        self.fields["story_points"].widget.attrs.update({
            'type':'number',
            'placeholder':'',
            'class':'input input-name',
            'id': 'name',
            'name': 'story_points',
            'readonly':'readonly',
        })
        self.fields["id_prioridad"].widget.attrs.update({
            'required': '',
            'class':'input ',
            'name': 'prioridad',
            'readonly':'readonly',
            'type':'number',

        })
        self.fields["id_estado"].widget.attrs.update({
            'required': '',
            'class':'input input-name',
            'name': 'estado',
            'readonly':'readonly',
        })
        self.fields["fecha_inicio"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_inicio',
            'readonly':'readonly',
        })
        self.fields["fecha_fin"].widget.attrs.update({
            'type':'date',
            'placeholder':'',
            'class':'input input-date',
            'id': 'name',
            'name': 'fecha_fin',
            'readonly':'readonly',
        })

        self.fields["definicion_hecho"].widget.attrs.update({
            'required': '',
            'placeholder':'',
            'class':'input input-description',
            'id': 'name',
            'name': 'definicion_hecho',
            'readonly':'readonly',
        })

    class Meta:
        model=UserStory
        fields=["user_story_name","descripcion","story_points","definicion_hecho","id_prioridad","id_estado","fecha_inicio","fecha_fin"]

        widgets = {
            # 'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            # 'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'definicion_hecho':forms.Textarea(attrs={'cols': 30, 'rows': 8}),
            'descripcion':forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }