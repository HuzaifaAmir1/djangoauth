# Generated by Django 4.0.3 on 2023-12-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispute', '0002_alter_dispute_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispute',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]