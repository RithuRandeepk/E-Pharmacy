# Generated by Django 5.0.1 on 2024-02-02 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.CharField(max_length=250, null=True),
        ),
    ]