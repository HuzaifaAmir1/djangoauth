# Generated by Django 4.0.3 on 2023-11-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='extras',
            field=models.JSONField(blank=True, null=True),
        ),
    ]