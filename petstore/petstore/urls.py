"""
URL configuration for petstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.profile1),
    path('index',views.index),
    path('about',views.about),
    path('blog',views.blog),
    path('contact',views.contact),
    path('detail',views.detail),
    path('adoption',views.adoption),
    path('product',views.product),
    path('service',views.service),
    path('team',views.team),
    path('testimonial',views.testimonial),
    path('login',views.edit),
    path('userreg',views.userreg),
    path('change',views.change),#changepwd.html
    path('chngepwd',views.chngepwd),
    path('signup.html', views.signup),
    path('log',views.log),
    path('logout',views.logout),
    path('profile',views.userprofile),

    #user
    path('userindex',views.userindex),
    path('userabout',views.userabout),
    path('userservice',views.userservice),
    path('userproduct',views.userproduct),
    path('useradoption',views.useradoption),
    # path('indexadoption',views.indexadoption),
    path('userteam',views.userteam),
    path('usertestimonial',views.usertestimonial),
    path('userblog',views.userblog),
    path('userdetail',views.userdetail),
    path('adopt',views.adopt),
    path('serviceapp',views.serviceapp),
    path('serviceappoinment',views.serviceappoinment),
    path('userserviceview',views.userserviceview),
    path('useradoptview',views.useradoptview),
    path('myorder',views.my_order),

    path('cart',views.cartview),
    path('add_cart/<int:i>',views.add_cart),
    path('add_cart1/<int:i>', views.add_cart1),
    path('quantity/<int:i>',views.quantity),
    path('quan_tity/<int:i>',views.quan_tity),
    path('wishlist',views.userwishlist),
    path('add_wishlist/<int:i>',views.add_wishlist),
    path('trash/<int:i>',views.trash),
    path('remove/<int:i>',views.remove),
    path('paymentform',views.paymentform),

    path('pay/<int:id>',views.pay),
    path('success',views.success),

    path('contactform',views.contactform),


    #admin
    path('adindex',views.adindex),
    path('adabout',views.adabout),
    path('adservice',views.disp_appoinment),
    # path('adproduct',views.adproduct),
    path('adadoption',views.adadoption),
    path('disp_req',views.disp_req),
    path('adopt_req', views.adopt_req),
    path("adserviceview",views.adserviceview),
    path("accept",views.accept),
    path("reject",views.reject),
    path("update",views.adopt_update),
    path("delete",views.adopt_delete),
    path('manage',views.manage),
    path('product_update/<int:i>',views.product_update),
    path('delete/<int:i>',views.delete),
    path('complaint',views.complaint),
    path('orders',views.orders),
    path('order_update/<int:i>',views.order_update),


    path('new',views.new),
    # path('update_prof',views.update_prof),
    path('update_prof',views.update_profile),
    path('up_prof',views.up_prof),

    path("add",views.add),
    path('add_product',views.add_product),
    path('adproduct',views.adproductview),
    path('adviewproduct',views.adviewproduct),
    path('add_adopt',views.add_adopt),
    # path('viewadopt',views.vviewadopt)

    path('productup',views.productup),

#forgot password
    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password)

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)