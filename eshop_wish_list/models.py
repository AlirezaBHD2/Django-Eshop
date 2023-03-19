from django.db import models
from eshop_product.models import Product

# Create your models here.
class Wish_List(models.Model):
    user = models.CharField(max_length=200, verbose_name='کاربر')
    products = models.ManyToManyField(Product , blank=True ,verbose_name='مجصولات')
    class Meta:
        verbose_name = 'لیست علاقه مندی ها'
        verbose_name_plural = 'لیست علاقه مندی ها'