# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User, Group

    
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         db_table = 'django_session'


class Proyecto(models.Model):
    backlog_id = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_inicio_real = models.DateField(blank=True, null=True)
    fecha_fin_real = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.backlog_id

    class Meta:
        db_table = 'proyecto'


class Sprint(models.Model):
    backlog_id_sprint = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_inicio_real = models.DateField(blank=True, null=True)
    fecha_fin_real = models.DateField(blank=True, null=True)
    backlog_id = models.ForeignKey(Proyecto, on_delete=models.CASCADE, db_column='backlog_id')
    nombre= models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)

    #def __str__(self):
        #return self.backlog_id

    class Meta:
        db_table = 'sprint'


class UsuarioProyecto(models.Model):
    id_usu_proy_rol = models.AutoField(primary_key=True)
    backlog = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE, db_column='id_group')
    rol_usuario = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.id_user.username

    class Meta:
        db_table = 'usuario_proyecto'
        unique_together = (('id_usu_proy_rol', 'backlog'),)


class PrioridadUserStory(models.Model):
    id_prioridad = models.AutoField(primary_key=True)
    nombre_prioridad = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_prioridad

    class Meta:
        db_table = 'prioridad_user_story'


class EstadosUserStory(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_estado

    class Meta:
        db_table = 'estados_user_story'


class ComentariosUserStory(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=500, blank=True, null=True)

    

    class Meta:
        db_table = 'comentarios_user_story'


class UserStory(models.Model):
    id_user_story = models.AutoField(primary_key=True)
    user_story_name = models.CharField(max_length=100)
    id_usu_proy_rol = models.ForeignKey(UsuarioProyecto, on_delete=models.SET_DEFAULT, default=None, null=True, db_column='id_usu_proy_rol')
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    story_points = models.IntegerField(blank=True, null=True)
    definicion_hecho = models.CharField(max_length=200)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    id_estado = models.ForeignKey(EstadosUserStory, on_delete=models.CASCADE, db_column='id_estado')
    backlog_id_sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, db_column='backlog_id_sprint', blank=True, null=True)
    id_prioridad = models.ForeignKey(PrioridadUserStory, on_delete=models.CASCADE, db_column='id_prioridad', blank=True, null=True)
    id_comentario = models.ForeignKey(ComentariosUserStory, on_delete=models.CASCADE, db_column='id_comentario', blank=True, null=True)
    #usuario = models.CharField(max_length=100)
    
   
    class Meta:
        db_table = 'user_story'