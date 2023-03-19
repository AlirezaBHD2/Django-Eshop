# Generated by Django 4.1.6 on 2023-03-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eshop_product', '0005_product_visit_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200, verbose_name='کاربر')),
                ('products', models.ManyToManyField(blank=True, to='eshop_product.product', verbose_name='مجصولات')),
            ],
        ),
    ]