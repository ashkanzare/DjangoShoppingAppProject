# Generated by Django 3.2.7 on 2021-10-02 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_address_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='language',
            field=models.CharField(choices=[('en-us', 'English'), ('fa-ir', 'Persian')], default='fa-ir', max_length=5),
        ),
    ]