# Generated by Django 3.2.7 on 2021-10-13 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_address_receiver_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeCoinWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.FloatField(default=0, verbose_name='سکه')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='مشتری')),
            ],
        ),
    ]