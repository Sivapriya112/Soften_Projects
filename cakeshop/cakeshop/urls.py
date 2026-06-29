"""
URL configuration for cakeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from cake import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/',admin.site.urls),
    path('about',views.about),
    path('',views.index),
    path('contact',views.contact),
    path('menu',views.menu),
    path('service',views.service),
    path('testimonial',views.testimonial),
    path('team',views.team),
    # path('login',views.login),
    path('admin_login',views.admin_login),
    path('user_login',views.user_login),
    path('dboy_login',views.dboy_login),
    path('registerr',views.registerr),
    path('dboy_reg',views.dboy_reg),
    path('employee_details',views.employee_details),
    path('accept/<int:d>', views.accept),
    path('reject/<int:d>', views.reject),
    path('bookingdetails', views.bookingdetails),
    path('sendto_dboy/<int:d>/<int:x>', views.sendto_dboy),
    path('order_requests', views.order_requests),
    path('delivery_details', views.delivery_details),
    # path('sendto_dboy/<int:d>/<int:x>', views.sendto_dboy),
    path('accept_order/<int:d>', views.accept_order),
    path('reject_order/<int:d>', views.reject_order),
    path('order_delivered/<int:d>', views.order_delivered),
    path('log',views.log),
    path('adminhome', views.adminhome),
    path('deliveryhome',views.deliveryhome),
    path('dboy_profile',views.dboy_profile),

    path('update_profile', views.update_profile),
    path('addproduct', views.addproduct),
    path('viewuser',views.view_user),
    path('userhome',views.userhome),
    path('addcart/<int:d>',views.addcart),
    path('mycart',views.mycart),

    path('addwhishlist/<int:d>',views.addwhishlist),
    path('mywhishlist',views.mywhishlist),
    path('remove_whishlist/<int:d>',views.remove_whishlist),
    path('display',views.display),
    path('manageproduct',views.manageproduct),
    path('delete/<int:d>', views.delete_product),
    path('update/<int:g>', views.update),
    path('increments/<int:d>', views.increments),
    path('decrements/<int:d>', views.decrements),
    path('remove/<int:d>',views.rem),
    path('wedding',views.wedding),
    path('birthday', views.Birthday),

    # path('forgot', views.forgot_password),
    # path('reset/<token>', views.reset_password),
    path('update/', views.update_profile),
    path('profile', views.profile,name='profile'),
    path('single_checkout/<int:d>',views.single_checkout),
    path('payment',views.payment),
    path('pay_razor/<int:a>', views.pay_razor),
    path('success', views.success),
    path('successs', views.successs),
    path('cart_checkout', views.cart_checkout),
    path('cart_payment', views.cart_payment),
    path('cart_pay_razor/<int:a>', views.cart_pay_razor),
    path('myaddress', views.myaddress),
    path('updateaddress', views.updateaddress),
    path('myorders', views.myorders),
    path('user_logout', views.user_logout),
    path('admin_logout', views.admin_logout),
    path('dboy_logout', views.dboy_logout),
    # path('logout',views.logout),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)