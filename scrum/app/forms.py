from django import forms
from .models import Proyecto
from django.contrib.auth.models import User, Group


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


class UsuarioProyectoFormulario(forms.Form):
    usuario=forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(),required=True)
    rol=forms.ModelChoiceField(queryset=Group.objects.all(),widget=forms.Select(),required=True)




