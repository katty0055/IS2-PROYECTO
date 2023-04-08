from django import forms
from .models import UsuarioProyecto
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ProyectoUsuarioModelForm(forms.ModelForm):
    class Meta:
        model=UsuarioProyecto
        fields=["id_user","id_group"]
'''
class UsuarioProyectoFormulario(forms.Form):
    usuario=forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(),required=True)
    rol=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(),required=True)
'''


class UsuarioProyectoFormulario(forms.ModelForm):
    class Meta:
        model:UsuarioProyecto
        fields="__all__"


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

