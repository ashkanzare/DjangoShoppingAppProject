# Generated by Django 3.2.7 on 2021-10-16 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('saved', 'saved')], default='فعال', max_length=10, verbose_name='وضعیت')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='مشتری')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('INITIAL', 'INITIAL'), ('WAITING_FOR_PAY', 'WAITING_FOR_PAY'), ('PROCESSING', 'PROCESSING'), ('SENT', 'SENT'), ('DELIVERED', 'DELIVERED'), ('CANCELED', 'CANCELED')], default='INITIAL', max_length=100, verbose_name='وضعیت سفارش')),
                ('shipping_type', models.CharField(choices=[('MESHOP', 'meshop'), ('POST', 'post')], max_length=50, verbose_name='نوع ارسال')),
                ('customer_discount', models.FloatField(default=0)),
                ('payment_method', models.CharField(choices=[('ONLINE', 'ONLINE'), ('CASH_ON_DELIVERY', 'CASH_ON_DELIVERY'), ('MECOIN', 'MECOIN')], default='ONLINE', max_length=100, verbose_name='نحوه ی پرداخت')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='تاریخ')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='customer.address', verbose_name='آدرس')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.cart', verbose_name='سبد خرید')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='تعداد')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.cart', verbose_name='سبد خرید')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول')),
                ('product_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productcolor', verbose_name='رنگ')),
                ('product_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productfactorproperty', verbose_name='ویژگی')),
            ],
        ),
    ]
