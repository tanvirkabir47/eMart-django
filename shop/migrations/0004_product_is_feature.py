# Generated by Django 5.0.6 on 2024-05-23 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_productgallery_options_alter_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_feature',
            field=models.BooleanField(default=False),
        ),
    ]
