"""
URL configuration for hack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('reg',views.reg),
    path('adminhome',views.adminhome),
    path('userhome',views.userhome),
    path('login',views.login),
    path('addproduct',views.addproduct),
    path('manageproduct',views.manageproduct),
    path('delete/<int:a>',views.delete),
    path('update/<int:a>',views.update),
    path('products',views.products),
    path('add_cart/<int:d>',views.add_cart),
    path('cart_view',views.cart_view),
    path('dec/<int:d>',views.dec),
    path('inc/<int:d>',views.inc),
    path('rem/<int:d>',views.rem),
    path('remo/<int:d>',views.remo),
    path('wish/<int:d>',views.wish),
    path('wish',views.wish_view),
    path('logout',views.logout),
    path('order_sum',views.order_sum),
    path('address',views.address),
    path('payment/<int:id>',views.payment),
    path('success',views.order),
    path('myorder',views.myorder),
    path('booking',views.booking),
    path('delivery_reg',views.delivery_reg),
    path('delivery_login',views.delivery_login),
    path('delivery_home',views.delivery_home),
    path('delivery_view',views.delivery_view),
    path('reject/<int:a>',views.reject),
    path('accept/<int:a>',views.accept),
    path('choose/<int:a>',views.choose),
    path('delivery_order',views.delivery_order),
    path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password),
    path('delivered/<int:a>',views.delivered),
    path('about',views.about),
    path('contact',views.contact),
    path('blog',views.blog),
    path('alert',views.alert),
    path('history',views.history),
    path('profile',views.profile)

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)