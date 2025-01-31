# Generated by Django 3.2 on 2021-11-25 17:16

import django.core.validators
from django.db import migrations, models


def copy_prices(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for order_item in OrderItem.objects.all():
        order_item.price = order_item.product.price
        order_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
            preserve_default=False,
        ),
        migrations.RunPython(copy_prices),
    ]
