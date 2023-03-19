import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from eshop_product.models import Product
from .forms import UserNewOrderForm
from .models import Order, OrderDetail
from django.http import HttpResponse, Http404
from zeep import Client


@login_required(login_url="/login")
def add_user_order_single(request, *args, **kwargs):
    order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if order is None:
        order = Order.objects.create(owner_id=request.user.id, is_paid=False)
    product_id = kwargs['productId']
    count = 1
    product = Product.objects.get_by_id(product_id)
    same_order = OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first())
    same_order_count = len(
        OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first()))
    if same_order_count == 1:
        print(same_order.first().count)
        same_order.update(count=str(count + int(same_order.first().count)))
    else:
        order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/login")
def delete_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get("detail_id")
    if detail_id is not None:
        # order_detail = OrderDetail.objects.get_queryset().get(id=detail_id)
        order_detail = OrderDetail.objects.filter(id=detail_id, order__owner_id=request.user.id)
        # OrderDetail.objects.filter(product_id=detail_id)
        if order_detail is not None:
            order_detail.delete()
    return redirect("/open-order")


@login_required(login_url="/login")  # can access to this function only when your login
def add_user_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)
    product = Product.objects.first()
    if new_order_form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id, is_paid=False)
        product_id = new_order_form.cleaned_data.get("product_id")
        count = new_order_form.cleaned_data.get("count")
        if count < 0:
            count = 1
        product = Product.objects.get_by_id(product_id)
        same_order = OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first())
        same_order_count = len(
            OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first()))
        if same_order_count == 1:
            # print(count)
            print(same_order.first().count)
            same_order.update(count=str(count + int(same_order.first().count)))
        else:
            order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)

    return redirect(f"/products/{product.id}/{product.title}")


@login_required(login_url="/login")
def user_open_order(request):
    context = {"order": None,
               "details": None,
               "total": 0,
               "taxation": 0,
               "F_total": 0}
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context["order"] = open_order
        context["details"] = open_order.orderdetail_set.all()
        context["total"] = open_order.get_total_price()
        context["taxation"] = context["total"] * 0.09
        context["F_total"] = context["total"] + context["taxation"]
    return render(request, "order/user_open_order.html", context)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for really server.


def send_request(request, *args, **kwargs):
    total_price = 0
    open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    if open_order is not None:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest(
            MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}")
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    raise Http404()


def verify(request, **kwargs):
    order_id = kwargs.get("order_id")
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'])
        if result.Status == 100:
            user_order = Order.objects.get_queryset().get(id=order_id)
            user_order.is_paid = True
            user_order.payment_date = time.time()
            user_order.refID = result.RefID
            user_order.save()

            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
