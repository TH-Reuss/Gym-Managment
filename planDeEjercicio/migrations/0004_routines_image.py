# Generated by Django 4.1.3 on 2022-11-30 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planDeEjercicio', '0003_alter_exerciseplans_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='routines',
            name='image',
            field=models.URLField(null=True),
        ),
    ]