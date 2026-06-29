from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(user_register)
admin.site.register(add_product)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(orders)
admin.site.register(delivery_boy_register)
admin.site.register(PasswordReset)
