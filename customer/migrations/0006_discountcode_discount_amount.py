# Generated by Django 3.2.7 on 2021-10-13 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_mecoinwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='discount_amount',
            field=models.FloatField(default=0),
        ),
    ]