from django.contrib import admin
from .import models

# Register your models here.

admin.site.register(models.UsuarioProyecto)
admin.site.register(models.Proyecto)
admin.site.register(models.PrioridadUserStory)
admin.site.register(models.EstadosUserStory)
admin.site.register(models.Sprint)