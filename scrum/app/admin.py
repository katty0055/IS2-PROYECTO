from django.contrib import admin
from .import models

# Register your models here.

admin.site.register(models.UsuarioProyecto)
admin.site.register(models.Proyecto)