from django.shortcuts import render, redirect
from .models import Wish_List
from eshop_product.models import Product
from django.http import HttpResponse


def add_wish_list(request, *args, **kwargs):
    user = request.user.id
    product_id = kwargs['productId']
    if Wish_List.objects.filter(user=user).first() == None:
        Wish_List.objects.create(user=user)
    Wish_List.objects.filter(user=user)[0].products.add(Product.objects.get(id=product_id))

    return redirect(request.META.get('HTTP_REFERER'))


def remove_wish_list(request, *args, **kwargs):
    user = request.user.id
    product_id = kwargs['productId']
    if Wish_List.objects.filter(user=user).first() != None:
        Wish_List.objects.filter(user=user)[0].products.remove(Product.objects.get(id=product_id))

    return redirect(request.META.get('HTTP_REFERER'))
