import os

from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{name}{ext}"
    return f"logo-image/{final_name}"


# Create your models here.

class SiteSetting(models.Model):
    siteTitle = models.CharField(max_length=150, verbose_name="عنوان سایت")
    address = models.CharField(max_length=150, verbose_name="آدرس")
    phone = models.CharField(max_length=150, verbose_name='تلفن')
    mobile = models.CharField(max_length=150, verbose_name='موبایل')
    fax = models.CharField(max_length=150, verbose_name='فکس')
    email = models.CharField(max_length=150, verbose_name='ایمیل')
    about_us = models.TextField(verbose_name="درباره ما", null=True, blank=True)
    logo_image = models.ImageField(upload_to=upload_image_path, blank=True, null=True, verbose_name="تصویر لوگو")

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'مدیریت سایت'

    def __str__(self):
        return self.address


class SocialMedia(models.Model):
    social_name = models.CharField(max_length=150, null=True, verbose_name="اسم شبکه فضای مجازی")
    social_link = models.CharField(max_length=150, null=True, verbose_name="لینک فضای مجازی")
    social_image = models.ImageField(upload_to=upload_image_path, blank=True, null=True,
                                     verbose_name="تصویر فضای مجازی")

    class Meta:
        verbose_name = 'تنظیمات فضای مجازی'
        verbose_name_plural = 'مدیریت فضای مجازی'
