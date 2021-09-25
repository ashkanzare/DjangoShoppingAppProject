# Generated by Django 3.2.7 on 2021-09-24 22:10

from django.db import migrations, models
import utils.utils_functions


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20210924_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdiscount',
            name='date',
            field=models.DateTimeField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='productdiscount',
            name='percent_mode',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=utils.utils_functions.image_path_generator),
        ),
    ]
