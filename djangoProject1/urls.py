"""e_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import home_page, get_email
from djangoProject1.views import header, footer, about_page
from django.conf import settings

# from e_shop import settings

urlpatterns = [
    path('', home_page),
    path('admin/', admin.site.urls),
    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    path('about-us', about_page),
    path('get-email', get_email),
    path('', include("eshop_account.urls")),
    path('', include("eshop_product.urls")),
    path('', include("eshop_order.urls")),
    path('', include("eshop_contact.urls")),
    path('', include("eshop_wish_list.urls")),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
