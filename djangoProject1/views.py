import itertools
from django.views.generic import ListView

from django.http import Http404
from django.shortcuts import render, redirect

from eshop_product.models import Product
from eshop_product_category.models import ProductCategory
from eshop_sliders.models import Slider
from eshop_settings.models import SiteSetting
from eshop_wish_list.models import Wish_List
from eshop_contact.forms import CreateEmailForm
from eshop_contact.models import EmailNews


# header code behind
def header(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting}
    return render(request, 'shared/Header.html', context)


def footer(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    contact_form = CreateEmailForm(request.POST or None)
    if contact_form.is_valid():
        email = contact_form.cleaned_data.get("email")
        if email not in EmailNews.objects.all():
            EmailNews.objects.create(email=email)
            print("D")
            print(email)
    context = {
        'setting': site_setting,
        'contact_form':contact_form
    }
    return render(request, 'shared/Footer.html', context)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def my_grouper2(iterable, num):
    y = [iterable[n:n + num] for n in range(len(iterable) - (num - 1))]
    return y


# TODO: comments / blog / add to liked list use ajax
# code behind
def home_page(request):
    categories = ProductCategory.objects.all()
    sliders = Slider.objects.all()
    most_visit_products = Product.objects.order_by("-visit_count").all()[:8]
    latest = Product.objects.order_by("-id").all()[:8]

    products_by_category = []

    for category in categories:
        products = Product.objects.all()
        same_category = []
        for product in products:
            if len(same_category) != 4 and product.categories.first() == category:
                same_category.append(product)
        products_by_category.append(same_category)
    wish_list = []
    if Wish_List.objects.filter(user=request.user.id).first():
        wish_list = Wish_List.objects.filter(user=request.user.id).first().products.all()

    context = {
        'data': 'این سایت فروشگاهی با فریم ورک django نوشته شده',
        "Sliders": sliders,
        "most_visit": list(most_visit_products[4:8]),
        "most_visit2": list(most_visit_products[:4]),
        "latest_products": list(latest[4:8]),
        "latest_products2": list(latest[:4]),
        'categories': categories,
        "products_by_category": products_by_category,
        "wish_list": wish_list

    }
    return render(request, 'home_page.html', context)


def about_page(request):
    site_setting = SiteSetting.objects.first()
    context = {'setting': site_setting}
    return render(request, "about_page.html", context)


class ProductsListByCategory(ListView):
    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = ProductCategory.objects.filter(name__iexact=category_name).first()
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        return Product.objects.get_products_by_category(category_name)

def get_email(request):
    contact_form = CreateContactForm(request.POST or None)
    if contact_form.is_valid():
        email = contact_form.cleaned_data.get("email")
        print("D")

    return redirect(request.META.get('HTTP_REFERER'))
