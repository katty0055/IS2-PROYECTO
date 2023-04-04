from django import forms
from .models import UsuarioProyecto
from django.contrib.auth.models import User, Group

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

