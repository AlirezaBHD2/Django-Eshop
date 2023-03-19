from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from eshop_product.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_paid = models.BooleanField(null=True, verbose_name="پرداخت شده")
    refID = models.IntegerField(null=True, verbose_name="کد پیگیری")
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید کاربران"

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        amount = 0
        for detail in self.orderdetail_set.all():
            amount = + detail.price * detail.count
        return amount


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.IntegerField(verbose_name="قیمت محصول")
    count = models.IntegerField(verbose_name="تعداد")

    def get_detail_sum(self):
        return self.count * self.price

    class Meta:
        verbose_name = "جزئیات محصول"
        verbose_name_plural = "اطلاعات جزئیات محصولات"

    def __str__(self):
        return self.product.title
