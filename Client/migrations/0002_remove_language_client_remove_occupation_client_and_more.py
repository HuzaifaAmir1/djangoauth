# Generated by Django 4.0.3 on 2023-11-28 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='client',
        ),
        migrations.RemoveField(
            model_name='occupation',
            name='client',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='client',
        ),
        migrations.RemoveField(
            model_name='client',
            name='description2',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.DeleteModel(
            name='Occupation',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
