# Generated by Django 4.1.7 on 2023-05-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_remove_proyecto_estado"),
    ]

    operations = [
        migrations.AddField(
            model_name="proyecto",
            name="estado",
            field=models.BooleanField(default=True),
        ),
    ]