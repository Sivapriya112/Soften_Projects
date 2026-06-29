from django.contrib import admin # type: ignore
from .models import user_details,services,BookingOrders,Products,UserWishlist,UserCarts,ProductsOrders,DeliveryBoy,ProductRate
# Register your models here.
admin.site.register(user_details)
admin.site.register(services)
admin.site.register(BookingOrders)
admin.site.register(Products)
admin.site.register(UserWishlist)
admin.site.register(UserCarts)
admin.site.register(ProductsOrders)
admin.site.register(DeliveryBoy)
admin.site.register(ProductRate)

