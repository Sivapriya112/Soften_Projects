"""
URL configuration for fish_shop project.

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
from myapps import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path('admin/', admin.site.urls),
     path('about',views.about),
     path('bloggrid',views.bloggrid),
     path('booking',views.booking),
     path('contact',views.contact),
     path('',views.index),
     path('service',views.service),
     path('blogdet',views.blogdetail),
     path('register',views.reg),
     path('login',views.login),
     path('forgot',views.forgot_password,name="forgot"),
     path('reset/<token>',views.reset_password,name='reset_password'),
     path('logout',views.logout),
     path('userhome',views.userhome),
     path('categories',views.categories),
     path('community',views.community),
     path('aggressive',views.aggressive),
     path('goldfish',views.goldfish),
     path('fighter',views.fighter),
     path('koicarp',views.koicarp),
     path('cart/<int:k>',views.add_cart),
     path('displaycart',views.display_cart),
     path('checkout_cart/<int:total>',views.checkoutcart,name='checkout_cart'),
     path('payment_cart/<int:amount>',views.pay_cart),
     path('deletecart/<int:d>',views.cart_delete),
     path('increment/<int:cart_id>',views.increment),
     path('decrement/<int:cart_id>',views.decrement_quantity),
     path('wishlist/<int:pid>',views.Wishlist),
     path('displaywishlist',views.display_wishlist),
     path('removewishlist/<int:d>',views.remove_wishlist),
     path('details/<int:d>', views.details),
     path('user_recent_orders', views.userrecentorders, name='user_recent_orders'),
     path('pay/<int:amount>',views.pay,name='pay'),
     path('success',views.success),
     path('logout',views.Log_out),
     path('profile', views.profile, name='profile'),
     path('update_profile', views.updateprofile),
      path('change_password', views.changepassword),
     path('description/<int:d>',views.fish_details),
     path('lowstock',views.low_stock),
     path('adminhome',views.adminhome),
     path('viewuser',views.viewuser),
     path('addproduct',views.add_product),
     path('display',views.display_product),
      path('productedit/<int:d>',views.admin_edit),
     path('productdelete/<int:k>',views.admin_delete),
     path('admin_order_details', views.admin_orders, name='admin_order_details'),
    path('admin_order_update/<int:d>', views.adminorderupdate),
     path('logout',views.logout),


]
if settings.DEBUG:
     urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
