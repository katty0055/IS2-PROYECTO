# Generated by Django 4.1.7 on 2023-07-02 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_proyecto_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstory',
            name='id_comentario',
        ),
        migrations.AddField(
            model_name='comentariosuserstory',
            name='us',
            field=models.ForeignKey(blank=True, db_column='id_user_story', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.userstory'),
        ),
    ]
