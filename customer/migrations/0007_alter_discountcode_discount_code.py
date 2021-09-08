# Generated by Django 3.2.7 on 2021-09-08 22:19

import django.core.validators
from django.db import migrations, models
import utils.utils_functions


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_discountcode_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='discount_code',
            field=models.CharField(default=utils.utils_functions.generate_random_string, max_length=8, validators=[django.core.validators.RegexValidator(message='شماره تلفن خود را بدون صفر وارد کنید. مانند : ۹۱۲۱۲۳۴۵۶۷', regex='[0-9]*')], verbose_name='کد تخفیف'),
        ),
    ]
