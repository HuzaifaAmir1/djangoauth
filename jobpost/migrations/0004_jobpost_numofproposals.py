# Generated by Django 4.0.3 on 2023-12-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpost', '0003_savedjob_job_post_savedjob_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='numofproposals',
            field=models.IntegerField(default=0),
        ),
    ]