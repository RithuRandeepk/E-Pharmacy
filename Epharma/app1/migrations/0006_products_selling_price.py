# Generated by Django 5.0.1 on 2024-02-06 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_uploadedfilemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='selling_price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
