# Generated by Django 3.2.7 on 2021-10-13 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20211013_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_discount',
            field=models.FloatField(default=0),
        ),
    ]
