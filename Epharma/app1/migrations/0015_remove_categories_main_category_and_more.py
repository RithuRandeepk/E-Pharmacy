# Generated by Django 4.2.7 on 2024-02-27 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_categories_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='main_category',
        ),
        migrations.AddField(
            model_name='categories',
            name='maincategory',
            field=models.CharField(max_length=250, null=True),
        ),
    ]