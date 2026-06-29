"""
URL configuration for AutoCar project.

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
from django.contrib import admin  # type: ignore
from django.urls import path,include  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static   # type: ignore
from Serv_Booking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('UserRegister',views.UserRegister),
    path('user_register',views.user_register),
    path('user_login',views.user_login),
    path('UserHome',views.UserHome),
    path('ServiceListing',views.ServiceListing),
    path('UserServices',views.UserServices),
    path('UserBooking/<int:i>',views.Userbooking),
    path('UserBooking2',views.Userbooking2),
    path('timeslot', views.timeslotbooking), 
    path('order', views.order),
    path('success', views.success), 
    path('forgot', views.forgot_password), 
    path('reset_password/<token>', views.reset_password), 
    path('UserBookingListing', views.UserBookingListing), 
    path('CancelBooking/<int:p>', views.CancelBooking),
    path('UserProfile', views.UserProfile),
    
    path('PayPending', views.PayPending),
    # products starts
     
    path('ProductsListing', views.products_listing), 
    path('SellProducts', views.SellProducts), 
    path('YourProducts', views.YourProducts), 
    path('increment/<int:i>', views.increment), 
    path('edit/<int:i>', views.Edit), 
    path('decrement/<int:i>', views.decrement), 
    path('wishlist/<int:i>', views.wishlist), 
    path('ViewWishList', views.ViewWishList), 
    path('AddCart/<int:i>', views.add_cart), 
    path('UserCart', views.user_cart), 
    path('CartIncrement/<int:i>', views.cart_increment), 
    path('CartDecrement/<int:i>', views.cart_decrement), 
    path('ProductDetails/<int:i>', views.product_details), 
    path('YourOrders', views.Yourorders), 
    path('ProductsPayment/<int:i>', views.ProductsPayment), 
    path('SingleProductsPayment/<int:i>', views.SingleProductsPayment), 
    path('OrderSuccess', views.OrderSuccess), 
    path('SingleOrderSuccess', views.SingleOrderSuccess), 
    path('BuyNow/<int:i>', views.BuyNow), 
    path('CancelOrder/<int:i>', views.CancelOrder), 
    path('Rate',views.Rate), 
    path('logout',views.logout),
    
    #Delivery Boy ===========================================
    path('DUserHome',views.DUserHome), 
    path('DUserProfile',views.DUserProfile), 
    path('DUserRegister', views.DUserRegister, name='DUserRegister'),
    path('DUserLogin', views.DUserLogin),
    path('Dforgot', views.Dforgot_password), 
    path('Dreset_password/<token>', views.Dreset_password), 
    path('DeliveryOrders', views.DeliveryOrders), 
    path('AcceptOrder/<int:i>', views.AcceptOrder), 
    path('DeliveryHistory', views.DeliveryHistory), 
    path('CancelDeliveryorder/<int:i>', views.CancelDeliveryorder), 
    path('deliveryotp/<int:i>', views.deliveryotp), 
    
    #Admin-------------------------------------
    path('AdminLogin',views.AdminLogin),
    path('AdminHome',views.AdminHome),
    path('AdminViewProducts',views.AdminViewProducts),
    path('UpdateProduct',views.UpdateProduct),
    path('UpdateImage/<int:i>', views.UpdateImage),
    path('DeleteProduct', views.DeleteProduct),
    path('AdminAddProducts', views.AdminAddProducts),
    path('AdminAddService', views.AdminAddService),
    path('AdminViewServices', views.AdminViewServices),
    path('UpdateService', views.UpdateService),
    path('DeleteService', views.DeleteService),
    path('StockUpdate', views.StockUpdate),
    path('ItemUpdate/<int:i>', views.ItemUpdate),
    path('StockFilter', views.StockFilter),
    path('ViewDeliveryBoys', views.ViewDeliveryBoys),
    path('ViewUsers', views.ViewUsers),
    path('DboyStatusUpdate', views.DboyStatusUpdate),
    path('UserStatusUpdate', views.UserStatusUpdate),
    path('UserDelete/<int:i>', views.UserDelete),
    path('ViewBookings', views.ViewBookings),
    path('UpdateBookingStatus', views.UpdateBookingStatus),
    path('RefundPayment<str:i>', views.RefundPayment),
    path('RefundSuccess', views.RefundSuccess),
    path('ProductRefundSuccess', views.ProductRefundSuccess),
    path('ProductOrdersView', views.ProductOrdersView),
    path('AddBooking', views.AddBooking),
    path('AdminTimeslot', views.AdminTimeslot), 
    path('AdminOrder', views.AdminOrder), 
    path('AdminPaymentOrderStatus', views.AdminPaymentOrderStatus), 
    path('Ratings', views.Ratings), 
    

    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)