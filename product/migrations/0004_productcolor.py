# Generated by Django 3.2.7 on 2021-09-27 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210926_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('aqua', '#00ffff'), ('black', '#000000'), ('blue', '#0000ff'), ('fuchsia', '#ff00ff'), ('green', '#008000'), ('gray', '#808080'), ('lime', '#00ff00'), ('maroon', '#800000'), ('navy', '#000080'), ('olive', '#808000'), ('purple', '#800080'), ('red', '#ff0000'), ('silver', '#c0c0c0'), ('teal', '#008080'), ('white', '#ffffff'), ('yellow', '#ffff00')], max_length=100)),
                ('price_impact', models.FloatField(default=0, verbose_name='تاثیر بر قیمت')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='موجودی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='رنگ')),
            ],
        ),
    ]