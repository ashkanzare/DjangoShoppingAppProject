# Generated by Django 3.2.7 on 2021-09-18 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=10000, unique=True, verbose_name='شماره تلفن'),
        ),
    ]
