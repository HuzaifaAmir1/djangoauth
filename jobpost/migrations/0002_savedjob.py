# Generated by Django 4.0.3 on 2023-11-28 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpost', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
