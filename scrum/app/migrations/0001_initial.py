from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentariosUserStory',
            fields=[
                ('id_comentario', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'comentarios_user_story',
            },
        ),
        migrations.CreateModel(
            name='EstadosUserStory',
            fields=[
                ('id_estado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'estados_user_story',
            },
        ),
        migrations.CreateModel(
            name='PrioridadUserStory',
            fields=[
                ('id_prioridad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_prioridad', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'prioridad_user_story',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('backlog_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'proyecto',
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('backlog_id_sprint', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('fecha_inicio_real', models.DateField()),
                ('fecha_fin_real', models.DateField()),
            ],
            options={
                'db_table': 'sprint',
            },
        ),
        migrations.CreateModel(
            name='UsuarioProyecto',
            fields=[
                ('id_usu_proy_rol', models.AutoField(primary_key=True, serialize=False)),
                ('rol_usuario', models.CharField(max_length=50)),
                ('backlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proyecto')),
                ('id_group', models.ForeignKey(db_column='id_group', on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('id_user', models.ForeignKey(db_column='id_user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_proyecto',
                'unique_together': {('id_usu_proy_rol', 'backlog')},
            },
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id_user_story', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('story_points', models.IntegerField(blank=True, null=True)),
                ('definicion_hecho', models.CharField(max_length=200)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('backlog_id_sprint', models.ForeignKey(blank=True, db_column='backlog_id_sprint', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.sprint')),
                ('id_comentario', models.ForeignKey(blank=True, db_column='id_comentario', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.comentariosuserstory')),
                ('id_estado', models.ForeignKey(db_column='id_estado', on_delete=django.db.models.deletion.CASCADE, to='app.estadosuserstory')),
                ('id_prioridad', models.ForeignKey(blank=True, db_column='id_prioridad', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.prioridaduserstory')),
                ('id_usu_proy_rol', models.ForeignKey(db_column='id_usu_proy_rol', on_delete=django.db.models.deletion.CASCADE, to='app.usuarioproyecto')),
            ],
            options={
                'db_table': 'user_story',
            },
        ),
    ]
