from django.db import models


# Create your models here.
class ContactUs(models.Model):
    full_name = models.CharField(null=True ,max_length=200, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(null=True ,max_length=150, verbose_name="ایمیل")
    subject = models.CharField(null=True ,max_length=200, verbose_name="عموان پیام")
    text = models.TextField(null=True ,verbose_name="متن پیام")
    is_read = models.BooleanField(null=True ,verbose_name="خوانده شده")

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس های کاربران'

    def __str__(self):
        return self.subject

class EmailNews(models.Model):
    email = models.EmailField(null=True ,max_length=150, verbose_name="ایمیل")

    class Meta:
        verbose_name = 'ایمیل کاربران'
        verbose_name_plural = 'ایمیل کاربران'

    def __str__(self):
        return self.email

