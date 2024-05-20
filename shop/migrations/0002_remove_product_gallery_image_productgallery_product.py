# Generated by Django 5.0.6 on 2024-05-20 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='gallery_image',
        ),
        migrations.AddField(
            model_name='productgallery',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product'),
            preserve_default=False,
        ),
    ]
