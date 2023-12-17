# Generated by Django 4.0.3 on 2023-11-29 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0002_remove_occupation_seller_alter_education_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='seller',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='Seller.seller'),
        ),
        migrations.AlterField(
            model_name='language',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='Seller.seller'),
        ),
    ]