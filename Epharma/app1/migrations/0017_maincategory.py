# Generated by Django 4.2.7 on 2024-02-27 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_remove_categories_maincategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maincategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maincategory', models.CharField(max_length=250, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]